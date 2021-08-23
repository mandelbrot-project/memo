from collections import Counter
import pandas as pd
import numpy as np

def generate_memo(doc_with_meta, quant_table):
    ''' 
    Use a doc_with_meta table and a quant_table to generate a MEMO matrix.
    Returns a pd.DataFrame MEMO matrix.
    '''
    quant_table[quant_table == 0] = np.nan
    merged_table = pd.merge(doc_with_meta[['scans', 'documents']], quant_table, left_on = "scans", right_index=True, how="inner") 
    samples_col = list(quant_table.columns)
    fingerprints = []
    for col in samples_col:
        merged_table[col] = np.where(~merged_table[col].isna(), merged_table['documents'], merged_table[col])
        col_list = merged_table[col].dropna().tolist()
        fingerprint = [item for sublist in col_list for item in sublist]
        cnt = Counter(fingerprint)
        fingerprints.append(cnt)
    memo_matrix = pd.DataFrame(fingerprints)
    memo_matrix.index = samples_col
    memo_matrix.fillna(0, inplace=True)
    return memo_matrix

def filter_memo(memo_matrix, blank_pattern, max_blank_occurence):
    ''' 
    Filter peak/loss occuring in more than max_blank_occurence blank samples + remove blank samples
    Returns a filtered pd.DataFrame MEMO matrix
    '''
    memo_matrix_blanks = memo_matrix[memo_matrix.index.str.contains(blank_pattern, case = False)]
    blank_samples = list(memo_matrix_blanks.index)
    memo_matrix_blanks = memo_matrix_blanks.loc[:, (memo_matrix_blanks != 0).any(axis=0)]
    count_null = memo_matrix_blanks.replace(0, np.nan).isnull().sum()
    excluded_features = count_null[count_null < (len(memo_matrix_blanks)-max_blank_occurence)].index

    memo_matrix_filtered = memo_matrix.drop(excluded_features, axis=1)
    memo_matrix_filtered = memo_matrix_filtered.drop(blank_samples, axis=0)
    memo_matrix_filtered = memo_matrix_filtered.astype(int)
    memo_matrix_filtered = memo_matrix_filtered.loc[:, (memo_matrix_filtered != 0).any(axis=0)]

    return memo_matrix_filtered