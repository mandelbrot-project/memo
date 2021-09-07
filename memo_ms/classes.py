from dataclasses import dataclass, field, InitVar
from collections import Counter
from spec2vec import SpectrumDocument
import pandas as pd
import numpy as np
import memo_ms.import_data as import_data
from tqdm import tqdm

@dataclass
class SpectraDocuments:
    
    path : str
    min_relative_intensity : float = 0.01
    max_relative_intensity : float  = 1.00
    min_peaks_required : int  = 10
    losses_from : int = 10
    losses_to : int = 200
    n_decimals : int = 2
    spectra : list = field(init=False)
    document : pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.spectra = import_data.load_and_filter_from_mgf(
            path = self.path,  min_relative_intensity = self.min_relative_intensity,
            max_relative_intensity = self.max_relative_intensity, loss_mz_from = self.losses_from,
            loss_mz_to = self.losses_to, n_required = self.min_peaks_required
            )
        self.document = self._spec2doc()
    
    def _spec2doc(self) -> pd.DataFrame:
        """
        Apply filters to spectra and convert them to words vectors with the number of specified decimals.
        Returns a pd.DataFrame with spectra "documents" and metadata.
        """
        documents = [SpectrumDocument(s, n_decimals=self.n_decimals) for s in self.spectra]
        doc_with_meta = pd.DataFrame(s.metadata for s in self.spectra)
        doc_with_meta['documents'] = list(doc.words for doc in documents)
        doc_with_meta.scans = doc_with_meta.scans.astype(int)
        return doc_with_meta


@dataclass
class FeatureTable:
    path : str
    quant_table : pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.quant_table = import_data.import_mzmine2_quant_table(path = self.path)
  
@dataclass
class MemoContainer:

    featuretable : InitVar[FeatureTable] = None
    spectradocuments : InitVar[SpectraDocuments] = None
    feature_matrix : pd.DataFrame = field(init=False)
    memo_matrix : pd.DataFrame = field(init=False)

    def __post_init__(self, featuretable, spectradocuments):
        if featuretable is None and spectradocuments is None:
            pass
        elif featuretable is None and spectradocuments is not None:
            raise ValueError("spectradocuments argument missing")
        elif featuretable is not None and spectradocuments is None:
            raise ValueError("featuretable argument missing")
        elif type(featuretable) != FeatureTable:
            raise TypeError ("featuretable argument must be of type FeatureTable")
        elif type(spectradocuments) != SpectraDocuments:
            raise TypeError ("spectradocuments argument must be of type SpectraDocuments")
        elif featuretable is not None and spectradocuments is not None:
            print('generating memo_matrix from input featuretable and spectradocument')
            self.memo_matrix = self._generate_memo(featuretable, spectradocuments)
            self.feature_matrix = featuretable.quant_table

    # def _generate_memo(self, featuretable, spectradocuments) -> pd.DataFrame:
    #     """
    #     Use a doc_with_meta table and a quant_table to generate a MEMO matrix.
    #     Returns a pd.DataFrame MEMO matrix.
    #     """
    #     quant_table = featuretable.quant_table.copy()
    #     samples_col = list(quant_table.index)
    #     document = spectradocuments.document[['scans', 'documents']].copy()
    #     quant_table = quant_table.transpose()
    #     quant_table[quant_table == 0] = np.nan
    #     merged_table = pd.merge(document, quant_table, left_on = "scans", right_index=True, how="inner") 
    #     fingerprints = []
    #     for col in samples_col:
    #         merged_table[col] = np.where(~merged_table[col].isna(), merged_table['documents'], merged_table[col])
    #         col_list = merged_table[col].dropna().tolist()
    #         fingerprint = [item for sublist in col_list for item in sublist]
    #         cnt = Counter(fingerprint)
    #         fingerprints.append(cnt)
    #     memo_matrix = pd.DataFrame(fingerprints)
    #     memo_matrix.index = samples_col
    #     memo_matrix.fillna(0, inplace=True)
    #     memo_matrix.index.name = 'filename'
    #     return memo_matrix

    def _generate_memo(self, featuretable, spectradocuments) -> pd.DataFrame:
        """
        Use a doc_with_meta table and a quant_table to generate a MEMO matrix.
        Returns a pd.DataFrame MEMO matrix.
        """

        quant_table = featuretable.quant_table.copy()
        document = spectradocuments.document[['scans', 'documents']].set_index('scans')['documents'].to_dict()
        quant_table[quant_table == 0] = float('nan')
        results = quant_table.stack().reset_index(level=1).groupby(level=0, sort=False)['row ID'].apply(list).to_dict()        
        for samples in tqdm(results):
            results[samples] = [document.get(item,item) for item in results[samples]]
            results[samples] = [ x for x in results[samples] if not isinstance(x, int)]
            results[samples] = [item for sublist in results[samples] for item in sublist]
            results[samples] = Counter(results[samples])
        memo_matrix = pd.DataFrame(results)
        memo_matrix = memo_matrix.transpose()
        memo_matrix.fillna(0, inplace=True)
        memo_matrix.index.name = 'filename'
        return memo_matrix
   
    def filter_matrix(self, matrix_to_use, samples_pattern, max_occurence):
        """ 
        Filter a feature table or a MEMO matrix: remove samples matching samples_pattern
        AND remove features occuring in more than n = max_occurence samples matched by samples_pattern
        """
        if matrix_to_use == 'memo_matrix':
            table = self.memo_matrix.copy()
        elif matrix_to_use == 'feature_matrix':
            table = self.feature_matrix.copy()
        else:
            raise ValueError('Invalid matrix_to_use value: choose one of [memo_matrix, feature_matrix]')

        table_blanks = table[table.index.str.contains(samples_pattern, case = False)]
        blank_samples = list(table_blanks.index)
        table_blanks = table_blanks.loc[:, (table_blanks != 0).any(axis=0)]
        count_null = table_blanks.replace(0, np.nan).isnull().sum()
        excluded_features = count_null[count_null < (len(table_blanks)-max_occurence)].index

        table_filtered = table.drop(excluded_features, axis=1)
        table_filtered = table_filtered.drop(blank_samples, axis=0)
        table_filtered = table_filtered.astype(float)
        table_filtered = table_filtered.loc[:, (table_filtered != 0).any(axis=0)]

        if matrix_to_use == 'memo_matrix':
            self.filtered_memo_matrix = table_filtered
        elif matrix_to_use == 'feature_matrix':
            self.filtered_feature_matrix = table_filtered
        return None

    def merge_memo(self, MemoContainer2, left, right, drop_not_in_common=False):
        output = MemoContainer()

        if type(MemoContainer2) != MemoContainer:
            raise TypeError ("merge_memo() MemoContainer argument must be a MemoContainer")

        if left == 'memo_matrix':
            table_left = self.memo_matrix
        elif left == 'filtered_memo_matrix':
            table_left = self.filtered_memo_matrix
        else:
            raise ValueError('Invalid left value: choose one of [memo_matrix, filtered_memo_matrix]')
        
        if right == 'memo_matrix':
            table_right = MemoContainer2.memo_matrix
        elif right == 'filtered_memo_matrix':
            table_right = MemoContainer2.filtered_memo_matrix
        else:
            raise ValueError('Invalid right value: choose one of [memo_matrix, filtered_memo_matrix]')
        
        if drop_not_in_common == True:
            result = table_left.append(table_right, sort=False).dropna(axis='columns').fillna(0)
        else:
            result = table_left.append(table_right, sort=False).fillna(0)
        output.memo_matrix = result
        return output

    def export_matrix(self, path, table = 'memo_matrix', sep = ','):
        if table == 'memo_matrix':
            self.memo_matrix.to_csv(path)
        elif table == 'feature_matrix':
            self.feature_matrix.to_csv(path)
        elif table == 'filtered_memo_matrix':
            self.filtered_memo_matrix.to_csv(path)
        elif table == 'filtered_feature_matrix':
            self.filtered_feature_matrix.to_csv(path)
        if table not in ['memo_matrix', 'feature_matrix', 'filtered_memo_matrix', 'filtered_feature_matrix']:
            raise ValueError('Invalid table value: choose one of [memo_matrix, feature_matrix, filtered_memo_matrix, filtered_feature_matrix]')            
        return None
