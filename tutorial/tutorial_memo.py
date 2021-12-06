# %% [markdown]
# # MEMO Tutorial on the Qemistree Evaluation Dataset

# %% [markdown]
# In this tutorial, we will use the Qemistree published dataset (https://doi.org/10.1038/s41589-020-00677-3) to apply the MS2 BasEd SaMple VectOrization (MEMO) method
# 
# The dataset is constitued of 2 fecal samples, 1 tomato sample and 1 plasma sample, plus different binary/quaternary mixtures of these four samples. Samples were profiled in UHPLC-MS/MS (Q-Exactive spectrometer) using 2 different LC-methods. Each sample was acquired in triplicates using each LC-method (see Qemistree paper for details).

# %% [markdown]
# ## First we import the needed packages
# Be sure to have first installed memo using 'pip install memo' within the memo environment. 
# Also make sure to launch this notebook using the memo conda environement.

# %%
import pandas as pd
import numpy as np
import memo_ms as memo
import plotly.express as px

# %%
# this cell is tagged 'parameters'
fake_parameter = 'foo'

# %% [markdown]
# With this step we import metadata:

# %%
pwd()

# %%

def conditions(df_meta):
    if ((df_meta['Proportion_Fecal_1']>0) & (df_meta['Proportion_Fecal_2']==0)& (df_meta['Proportion_Tomato']==0) & (df_meta['Proportion_NIST_1950_SRM']==0)):
        return 'Fecal_1'
    if ((df_meta['Proportion_Fecal_1']==0) & (df_meta['Proportion_Fecal_2']>0)& (df_meta['Proportion_Tomato']==0) & (df_meta['Proportion_NIST_1950_SRM']==0)):
        return 'Fecal_2'
    if ((df_meta['Proportion_Fecal_1']==0) & (df_meta['Proportion_Fecal_2']==0)& (df_meta['Proportion_Tomato']>0) & (df_meta['Proportion_NIST_1950_SRM']==0)):
        return 'Tomato'
    if ((df_meta['Proportion_Fecal_1']==0) & (df_meta['Proportion_Fecal_2']==0)& (df_meta['Proportion_Tomato']==0) & (df_meta['Proportion_NIST_1950_SRM']>0)):
        return 'Plasma'
    if ((df_meta['Proportion_Fecal_1']>0) & (df_meta['Proportion_Fecal_2']>0)& (df_meta['Proportion_Tomato']==0) & (df_meta['Proportion_NIST_1950_SRM']==0)):
        return 'Fecal_1 + Fecal_2'
    if ((df_meta['Proportion_Fecal_1']>0) & (df_meta['Proportion_Fecal_2']==0)& (df_meta['Proportion_Tomato']>0) & (df_meta['Proportion_NIST_1950_SRM']==0)):
        return 'Fecal_1 + Tomato'
    if ((df_meta['Proportion_Fecal_1']>0) & (df_meta['Proportion_Fecal_2']==0)& (df_meta['Proportion_Tomato']==0) & (df_meta['Proportion_NIST_1950_SRM']>0)):
        return 'Fecal_1 + Plasma'
    if ((df_meta['Proportion_Fecal_1']==0) & (df_meta['Proportion_Fecal_2']>0)& (df_meta['Proportion_Tomato']>0) & (df_meta['Proportion_NIST_1950_SRM']==0)):
        return 'Fecal_2 + Tomato'
    if ((df_meta['Proportion_Fecal_1']==0) & (df_meta['Proportion_Fecal_2']>0)& (df_meta['Proportion_Tomato']==0) & (df_meta['Proportion_NIST_1950_SRM']>0)):
        return 'Fecal_2 + Plasma'
    if ((df_meta['Proportion_Fecal_1']==0) & (df_meta['Proportion_Fecal_2']==0)& (df_meta['Proportion_Tomato']>0) & (df_meta['Proportion_NIST_1950_SRM']>0)):
        return 'Tomato + Plasma'
    if ((df_meta['Proportion_Fecal_1']>0) & (df_meta['Proportion_Fecal_2']>0)& (df_meta['Proportion_Tomato']>0) & (df_meta['Proportion_NIST_1950_SRM']>0)):
        return 'Fecal_1 + Fecal_2 + Tomato + Plasma' 
    else:
        return 'What is it? :)'


df_meta = pd.read_csv("../data/1901_gradient_benchmarking_dataset_v4_sample_metadata.txt", sep='\t')
df_meta['Samplename'] = df_meta['Samplename'].str[:-6]
df_meta['Samplename'] = df_meta['Samplename'].str.replace('BLANK_', 'BLANK')
df_meta = df_meta[['Filename', 'Experiment', 'Samplename', 'Triplicate_number', 'Proportion_Fecal_1', 'Proportion_Fecal_2', 'Proportion_Tomato', 'Proportion_NIST_1950_SRM']]
df_meta['contains'] = df_meta.apply(conditions, axis=1)
df_meta['instrument'] = np.where(df_meta['Samplename'].str.contains('qTOF'), 'qTOF', 'QE')
df_meta['blank_qc'] = np.where(df_meta['Samplename'].str.contains('blank|qcmix', case = False), 'yes', 'no')
df_meta


# %% [markdown]
# ## Import feature_quant table
# To compute the MEMO matrix of the dataset, we need the table reporting presence/absence of each metabolite in each sample. This information is in the quant table and we create a memo.FeatureTable dataclass object to load it.

# %%
feat_table_qe = memo.FeatureTable(path="../data/quantification_table-00000.csv", software='mzmine')
feat_table_qe.feature_table

# %% [markdown]
# ## Import spectra
# Since MEMO relies on the occurence of MS2 fragments/losses in samples to compare them, we obviously need to importthe features' fragmentation spectra. Losses are computed and spectra translated into documents. Store in memo.SpectraDocuments dataclass object.

# %%
spectra_qe = memo.SpectraDocuments(path="../data/qemistree_specs_ms.mgf", min_relative_intensity = 0.01,
            max_relative_intensity = 1, min_peaks_required=5, losses_from = 10, losses_to = 200, n_decimals = 2)
spectra_qe.document

# %% [markdown]
# ## Generation of MEMO matrix
# 
# Using the generated documents and the quant table, we can now obtain the MEMO matrix. The MEMO matrix is stored in the MemoContainer object, along with the feature table and the documents

# %%
memo_qe = memo.MemoMatrix()
memo_qe.memo_from_aligned_samples(feat_table_qe, spectra_qe)
memo_qe.memo_matrix

# %%
memo_qe = memo_qe.filter(samples_pattern='blank')
feat_table_qe = feat_table_qe.filter(samples_pattern='blank')
memo_qe.memo_matrix

# %% [markdown]
# 

# %% [markdown]
# ## Plotting
# 
# We can now use the MEMO matrix to generate the PCoA of our samples

# %%

memo.visualization.plot_pcoa_2d(
    matrix= memo_qe.memo_matrix,
    df_metadata=df_meta,
    metric= 'braycurtis',
    filename_col = 'Filename',
    group_col='contains',
    norm = False,
    scaling= False,
    pc_to_plot = [1,2]
)

# %%
memo.visualization.plot_pcoa_3d(
    matrix= memo_qe.memo_matrix,
    df_metadata=df_meta,
    metric= 'braycurtis',
    filename_col = 'Filename',
    group_col='contains',
    norm = False,
    scaling= False,
    pc_to_plot = [1,2,3]
)

# %%
df_meta_sub = df_meta[df_meta['Triplicate_number'] == 1]

memo.visualization.plot_heatmap(
    matrix= memo_qe.memo_matrix,
    df_metadata=df_meta_sub,
    filename_col = 'Filename',
    group_col = 'contains',
    plotly_discrete_cm = px.colors.qualitative.Plotly,
    linkage_method='ward',
    linkage_metric = 'euclidean',
    heatmap_metric = 'braycurtis',
    norm = False,
    scaling= False
)

# %%
memo.visualization.plot_hca(
    matrix= memo_qe.memo_matrix,
    df_metadata=df_meta_sub,
    filename_col = 'Filename',
    group_col = 'contains',
    linkage_method='ward',
    linkage_metric = 'euclidean',
    norm = False,
    scaling= False
)

# %% [markdown]
# ## Merge MEMO matrix from different MzMine projects

# %% [markdown]
# First, we load as before the spectra and feature matrix to generate the memo matrix of the different projects to merge.
# 
# In this case, we will once again use the Qemistree dataset and compare for the same samples data aquired on a QToF with some on a Q-Exactive (Orbitrap).

# %%
# Generate MEMO matrix for QE data

feat_table_qe = memo.FeatureTable(path="../data/qe_qtof_coanalysis/qe_quant_nogapF.csv", software='mzmine')
spectra_qe = memo.SpectraDocuments(path="../data/qe_qtof_coanalysis/qe_spectra_nogapF.mgf", min_relative_intensity = 0.01,
            max_relative_intensity = 1, min_peaks_required=5, losses_from = 10, losses_to = 200, n_decimals = 2)
memo_qe = memo.MemoMatrix()
memo_qe.memo_from_aligned_samples(feat_table_qe, spectra_qe)

# %%
# Generate MEMO matrix for QToF data

feat_table_qtof = memo.FeatureTable(path="../data/qe_qtof_coanalysis/qtof_quant_nogapF.csv", software='mzmine')
spectra_qtof = memo.SpectraDocuments(path="../data/qe_qtof_coanalysis/qtof_spectra_nogapF.mgf", min_relative_intensity = 0.01,
            max_relative_intensity = 1, min_peaks_required=5, losses_from = 10, losses_to = 200, n_decimals = 2)
memo_qtof = memo.MemoMatrix()
memo_qtof.memo_from_aligned_samples(feat_table_qtof, spectra_qtof)

# %%
memo_qe = memo_qe.filter(samples_pattern='blank')
memo_qtof = memo_qtof.filter(samples_pattern='blank')

# %% [markdown]
# Now, let's merge our 2 MEMO matrix. There is one paramater, drop_not_in_common, to decide wether to keep only shared peaks/losses or all of them.

# %%
memo_merged = memo_qe.merge_memo(memo_qtof, drop_not_in_common=True)

# %% [markdown]
# PCoA plot of the first 2 components show that the main parameter to discriminate our samples is the Instrument

# %%

memo.visualization.plot_pcoa_2d(
    matrix= memo_merged.memo_matrix,
    df_metadata=df_meta,
    metric= 'braycurtis',
    filename_col = 'Filename',
    group_col='contains',
    norm = True,
    scaling= False,
    pc_to_plot = [1,2]
)

# %% [markdown]
# But when looking at component 2 and 3, we see that it is possible to cluster chemically related samples using this approach.

# %%

memo.visualization.plot_pcoa_2d(
    matrix= memo_merged.memo_matrix,
    df_metadata=df_meta,
    metric= 'braycurtis',
    filename_col = 'Filename',
    group_col='contains',
    norm = True,
    scaling= False,
    pc_to_plot = [2,3]
)

# %%



