"""This test is meant to run a full example of a typical user workflow.
So far, I only copied part of the tutorial notebook.
TODO: Make meaningfull, clear workflow out of it.
"""
import memo_ms as memo
import numpy as np
import os
import pandas as pd
# import plotly.express as px
import pytest


PATH_ROOT = os.path.dirname(os.path.dirname((__file__)))
PATH_TEST_RESOURCES = os.path.join(PATH_ROOT, 'data')


@pytest.mark.integtest
def test_workflow():
    def conditions(df_meta):
        return_strings = []
        if df_meta['Proportion_Fecal_1'] > 0:
            return_strings.append("Fecal_1")
        if df_meta['Proportion_Fecal_2'] > 0:
            return_strings.append("Fecal_2")
        if df_meta['Proportion_Tomato'] > 0:
            return_strings.append("Tomato")
        if df_meta['Proportion_NIST_1950_SRM'] > 0:
            return_strings.append("Plasma")

        if len(return_strings) > 0:
            return " + ".join(return_strings)
        return 'What is it? :)'

    metadata_filename = os.path.join(PATH_TEST_RESOURCES, "1901_gradient_benchmarking_dataset_v4_sample_metadata.txt")
    df_meta = pd.read_csv(metadata_filename, sep='\t')
    df_meta['Samplename'] = df_meta['Samplename'].str[:-6]
    df_meta['Samplename'] = df_meta['Samplename'].str.replace('BLANK_', 'BLANK')
    df_meta = df_meta[['Filename', 'Experiment', 'Samplename', 'Triplicate_number', 'Proportion_Fecal_1', 'Proportion_Fecal_2', 'Proportion_Tomato', 'Proportion_NIST_1950_SRM']]
    df_meta['contains'] = df_meta.apply(conditions, axis=1)
    df_meta['instrument'] = np.where(df_meta['Samplename'].str.contains('qTOF'), 'qTOF', 'QE')
    df_meta['blank_qc'] = np.where(df_meta['Samplename'].str.contains('blank|qcmix', case = False), 'yes', 'no')
    print(df_meta)

    # Import feature_quant table
    # To compute the MEMO matrix of the dataset, we need the table reporting presence/absence of each metabolite in each sample. This information is in the quant table and we create a memo.FeatureTable dataclass object to load it.

    table_filename = os.path.join(PATH_TEST_RESOURCES, "quantification_table-00000.csv")
    feat_table_qe = memo.FeatureTable(path=table_filename, software="mzmine")
    feat_table_qe.feature_table
    assert feat_table_qe.feature_table.shape == (198, 7032), \
        "Expected different table shape after filtering"
    # Import spectra
    # Since MEMO relies on the occurence of MS2 fragments/losses in samples to compare them, we obviously need to importthe features' fragmentation spectra. Losses are computed and spectra translated into documents. Store in memo.SpectraDocuments dataclass object.

    specs_filename = os.path.join(PATH_TEST_RESOURCES, "qemistree_specs_ms.mgf")
    spectra_qe = memo.SpectraDocuments(path=specs_filename, min_relative_intensity = 0.01,
                max_relative_intensity = 1, min_peaks_required=5, losses_from = 10, losses_to = 200, n_decimals = 2)
    spectra_qe.document    
    assert spectra_qe.document.shape == (6569, 6), \
        "Expected different table shape after filtering"

    # Generation of MEMO matrix
    # Using the generated documents and the quant table, we can now obtain the MEMO matrix. The MEMO matrix is stored in the MemoContainer object, along with the feature table and the documents
    memo_qe = memo.MemoMatrix()
    memo_qe.memo_from_aligned_samples(feat_table_qe, spectra_qe)
    memo_qe.memo_matrix    
    assert memo_qe.memo_matrix.shape == (198, 30324), \
        "Expected different table shape after filtering"

    memo_qe = memo_qe.filter(use_samples_pattern =True, samples_pattern='blank')    
    assert memo_qe.memo_matrix.shape == (171, 30324), \
        "Expected different table shape after filtering"
        
    feat_table_qe = feat_table_qe.filter(use_samples_pattern = True, samples_pattern='blank')    
    assert feat_table_qe.feature_table.shape == (171, 7032), \
        "Expected different table shape after filtering"
    
    memo_qe = memo_qe.filter(use_samples_pattern = False, max_rel_occurence=0.8, min_rel_occurence=0.2)    
    assert memo_qe.memo_matrix.shape == (171, 11666), \
        "Expected different table shape after filtering"
    