from dataclasses import dataclass, field
from collections import Counter
from spec2vec import SpectrumDocument
import pandas as pd
import numpy as np
from memo_ms import import_data
from tqdm import tqdm
import os


def filter_table(table, samples_pattern, max_occurence = None):
    
    table_matched = table[table.index.str.contains(samples_pattern, case = False)]
    matched_samples = list(table_matched.index)
    table_matched = table_matched.loc[:, (table_matched != 0).any(axis=0)]
    count_null = table_matched.replace(0, np.nan).isnull().sum()
    
    if max_occurence is not None:
        excluded_features = count_null[count_null < (len(table_matched)-max_occurence)].index
        table_filtered = table.drop(excluded_features, axis=1)
    else: 
        table_filtered = table
    
    table_filtered = table_filtered.drop(matched_samples, axis=0)
    table_filtered = table_filtered.astype(float)
    table_filtered = table_filtered.loc[:, (table_filtered != 0).any(axis=0)]
    
    return table_filtered
    
@dataclass
class SpectraDocuments:
    """Create a SpectraDocuments dataclass object containing spectra documents and metadata
    from an MzMine 2 spectra file (.mgf)

    Args:
        path (str): Path to spectra file (.mgf)
        min_relative_intensity (float): Minimal relative intensity to keep a peak
        max_relative_intensity (float): Maximal relative intensity to keep a peak
        min_peaks_required (int): Minimum number of peaks to keep a spectrum
        losses_from (int): minimal m/z value for losses
        losses_to (int): maximal m/z value for losses
        n_decimals (int): number of decimal when translating peaks/losses into words

    Returns:
        self.document (DataFrame): A table containing spectra documents and metadata
    """
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
    """Create a FeatureTable dataclass object from a feature table

    Args:
        path (str): Path to a feature table file (.csv)
        software (str): One of [mzmine, xcms, msdial]: the software used for feature detection

    Returns:
        self.feature_table (DataFrame): A cleaned feature quantification table
    """
    path : str
    software : str
    feature_table : pd.DataFrame = field(init=False)

    def __post_init__(self):
        if self.software == 'mzmine':
            self.feature_table = import_data.import_mzmine2_quant_table(path = self.path)
        elif self.software == 'xcms':
            self.feature_table = import_data.import_xcms_quant_table(path = self.path)
        elif self.software == 'msdial':
            self.feature_table = import_data.import_msdial_quant_table(path = self.path)
        else:
            raise ValueError("software argument missing, choose one of the currently supported pre-processing softwares: [mzmine, xcms, msdial]")
        
    def filter(self, samples_pattern, max_occurence = None):
        """Filter a feature table: remove samples matching samples_pattern
        AND remove features occuring in more than n = max_occurence samples matched by samples_pattern

        Args:
            samples_pattern (str): the str pattern to match in samples to filter
            max_occurence (int): maximal number of occurence allowed in matched samples before removing a feature/word

        Returns:
            self.filtered_feature_table (DataFrame): A filtered feature table
        """
        self.feature_table = filter_table(self.feature_table, samples_pattern, max_occurence)            
        return self
    
    def export_matrix(self, path, sep = ','):
        """Export a given matrix

        Args:
            path (str): path to export
            sep (str): separator

        Returns:
            None
        """   
        self.feature_table.to_csv(path, sep=sep)
    
@dataclass
class MemoMatrix:
    """Create an empty MemoMatrix dataclass object
    """
    def memo_from_aligned_samples(self, featuretable, spectradocuments) -> pd.DataFrame:
        """
        Use a featuretable and a spectradocuments to generate a MEMO matrix.
        Returns a pd.DataFrame MEMO matrix.

        Args:
            featuretable (FeatureTable): a FeatureTable dataclass object
            spectradocuments (SpectraDocuments): a SpectraDocuments dataclass oject

        Returns:
            self.memo_matrix (DataFrame): A MEMO matrix
        """
        if featuretable is None:
            raise ValueError("featuretable argument missing")
        if spectradocuments is None:
            raise ValueError("spectradocuments argument missing")
        if not isinstance(featuretable, FeatureTable):
            raise TypeError("featuretable argument must be of type FeatureTable")
        if not isinstance(spectradocuments, SpectraDocuments):
            raise TypeError("spectradocuments argument must be of type SpectraDocuments")
        print('generating memo_matrix from input featuretable and spectradocument')

        feature_table = featuretable.feature_table.copy()
        document = spectradocuments.document[['scans', 'documents']].set_index('scans')['documents'].to_dict()
        feature_table[feature_table == 0] = float('nan')
        results = feature_table.stack().reset_index(level=1).groupby(level=0, sort=False)['feature_id'].apply(list).to_dict()        
        for samples in tqdm(results):
            results[samples] = [document.get(item,item) for item in results[samples]]
            results[samples] = [ x for x in results[samples] if not isinstance(x, int)]
            results[samples] = [item for sublist in results[samples] for item in sublist]
            results[samples] = Counter(results[samples])
        memo_matrix = pd.DataFrame(results)
        memo_matrix = memo_matrix.transpose()
        memo_matrix.fillna(0, inplace=True)
        memo_matrix.index.name = 'filename'
        self.memo_matrix = memo_matrix
        self.filtered_memo_matrix = None
        self.filtered_feature_matrix = None

    def memo_from_unaligned_samples(self, path_to_samples_dir, min_relative_intensity = 0.01,
    max_relative_intensity = 1.00, min_peaks_required = 10, losses_from = 10, losses_to = 200, n_decimals = 2):
        """Generate a Memo matrix from a list of individual .mgf files

        Args:
            path_to_samples_dir (str): Path to the directory where individual .mgf files are gathered
            min_relative_intensity (float): Minimal relative intensity to keep a peak
            max_relative_intensity (float): Maximal relative intensity to keep a peak
            min_peaks_required (int): Minimum number of peaks to keep a spectrum
            losses_from (int): minimal m/z value for losses
            losses_to (int): maximal m/z value for losses
            n_decimals (int): number of decimal when translating peaks/losses into words

        Returns:
            self.memo_matrix (DataFrame): A MEMO matrix
        """
        #pylint: disable=too-many-arguments
        dic_memo = {}
        mgf_file = []
        for file in os.listdir(path_to_samples_dir):
            if file.endswith(".mgf"):
                mgf_file.append(file)
        for file in tqdm(mgf_file):
            spectra = import_data.load_and_filter_from_mgf(
                path = os.path.join(path_to_samples_dir, file), min_relative_intensity = min_relative_intensity,
                max_relative_intensity = max_relative_intensity, loss_mz_from = losses_from, loss_mz_to = losses_to, n_required = min_peaks_required
                )

            documents = [SpectrumDocument(s, n_decimals= n_decimals) for s in spectra]
            documents = list(doc.words for doc in documents)
            documents = [item for sublist in documents for item in sublist]
            documents = dict(Counter(documents))
            dic_memo[file.removesuffix('.mgf')] = documents

        self.memo_matrix = pd.DataFrame.from_dict(dic_memo, orient='index').fillna(0)

    def filter(self, samples_pattern, max_occurence = None):
        """Filter a MEMO matrix: remove samples matching samples_pattern
        AND remove features occuring in more than n = max_occurence samples matched by samples_pattern

        Args:
            samples_pattern (str): the str pattern to match in samples to filter
            max_occurence (int): maximal number of occurence allowed in matched samples before removing a feature/word

        Returns:
            self.filtered_memo_matrix (DataFrame): A filtered feature table matrix
        """
        self.memo_matrix = filter_table(self.memo_matrix, samples_pattern, max_occurence)        
        return self

    def merge_memo(self, memomatrix_2, drop_not_in_common=False):
        """Merge 2 MEMO matrix

        Args:
            memocontainer2 (MemoContainer): MemoMatrix dataclass object containing the 2nd MEMO matrix to merge
            drop_not_in_common (bool): Drop peaks/losses not in common
            
        Returns:
            MemoContainer (MemoContainer): A MemoMatrix dataclass object containing the merged MEMO matrix
        """
        output = MemoMatrix()

        if not isinstance(memomatrix_2, MemoMatrix):
            raise TypeError ("merge_memo() memomatrix_2 argument must be a MemoMatrix")

        table_left = self.memo_matrix
        table_right = memomatrix_2.memo_matrix
        
        if drop_not_in_common is True:
            result = table_left.append(table_right, sort=False).dropna(axis='columns').fillna(0)
        else:
            result = table_left.append(table_right, sort=False).fillna(0)
        output.memo_matrix = result
        return output

    def export_matrix(self, path, sep = ','):
        """Export a given matrix

        Args:
            path (str): path to export
            sep (str): separator
            
        Returns:
            None
        """      
        self.memo_matrix.to_csv(path, sep=sep)
