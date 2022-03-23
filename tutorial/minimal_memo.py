import argparse

import memo_ms as memo
import pandas as pd
import plotly.express as px

## parse CLI arguments
parser = argparse.ArgumentParser(description='Quick and dirty MEMO')
parser.add_argument(
    'features_table',
    type=str,
    nargs=1,
)
parser.add_argument(
    'spectra_file',
    type=str,
    nargs=1,
)
parser.add_argument(
    'metadata_table',
    type=str,
    nargs=1,
)
args = parser.parse_args()

## metadata step
df_meta = pd.read_csv(args.metadata_table[0])

## feature table step
feat_table_qe = memo.FeatureTable(
    path=args.features_table[0],
    software='mzmine'
)

## spectra step
spectra_qe = memo.SpectraDocuments(
    path=args.spectra_file[0],
    min_relative_intensity=0.01,
    max_relative_intensity=1,
    min_peaks_required=5,
    losses_from=10,
    losses_to=200,
    n_decimals=2
)

## memo matrix step
memo_qe = memo.MemoMatrix()
memo_qe.memo_from_aligned_samples(feat_table_qe, spectra_qe)

## visualization step
memo.visualization.plot_pcoa_2d(
    matrix=memo_qe.memo_matrix,
    df_metadata=df_meta,
    metric='braycurtis',
    filename_col='Filename',
    group_col='Group',
    norm=False,
    scaling=False,
    pc_to_plot=[1, 2]
)

memo.visualization.plot_heatmap(
    matrix=memo_qe.memo_matrix,
    df_metadata=df_meta,
    filename_col='Filename',
    group_col='Group',
    plotly_discrete_cm=px.colors.qualitative.Plotly,
    linkage_method='ward',
    linkage_metric='euclidean',
    heatmap_metric='braycurtis',
    norm=False,
    scaling=False
)

memo.visualization.plot_hca(
    matrix=memo_qe.memo_matrix,
    df_metadata=df_meta,
    filename_col='Filename',
    group_col='Group',
    linkage_method='ward',
    linkage_metric='euclidean',
    norm=False,
    scaling=False
)
