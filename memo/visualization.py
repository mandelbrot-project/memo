import pandas as pd
import numpy as np
import scipy as sp
from skbio.stats.ordination import pcoa
import cimcb_lite as cb
import plotly.express as px

def plot_pcoa_2d(memo_matrix, df_metadata, filename_col, color, metric = 'braycurtis', norm = False, scaling = False, pc_to_plot = [1,2]):
    '''
    Compute distance matrix and perform PCoA on it from a given MEMO matrix
    Output 2D score plot, distance matrix and skbio.pcoa 

    plot_pcoa_2d(memo_matrix, df_metadata, filename_col, color, metric = 'braycurtis', norm = False, scaling = False, pc_to_plot = [1,2])
    Args:
        memo_matrix
        df_metadata
        filename_col
        color
        metric
        norm
        scaling
        pc_to_plot
    '''

    df_metadata_resticted = df_metadata[df_metadata[filename_col].isin(list(memo_matrix.index))]
    memo_matrix = memo_matrix[memo_matrix.index.isin(list(df_metadata_resticted.Filename))].reindex(list(df_metadata_resticted.Filename))
    if norm == True:
        memo_matrix = memo_matrix.div(memo_matrix.sum(axis=1), axis=0)
    if scaling == True:
        memo_matrix = memo_matrix.to_numpy()
        memo_matrix = np.where(memo_matrix== 0, 0.1, memo_matrix)         
        memo_matrix = np.log10(memo_matrix) # Log scale (base-10)
        memo_matrix = np.where(memo_matrix== -1, 0, memo_matrix)         
        memo_matrix = cb.utils.scale(memo_matrix, method='pareto')

    dm_memo = sp.spatial.distance.pdist(memo_matrix, metric)
    pcoa_results = pcoa(dm_memo)

    x = pcoa_results.samples[f'PC{pc_to_plot[0]}']
    y = pcoa_results.samples[f'PC{pc_to_plot[1]}']

    
    exp_var_pc1 = round(100*pcoa_results.proportion_explained[pc_to_plot[0] - 1 ], 1)
    exp_var_pc2 = round(100*pcoa_results.proportion_explained[pc_to_plot[1] - 1 ], 1)

    fig = px.scatter(x=x, y=y, color=df_metadata_resticted[color],
    labels={'x': f"PC{pc_to_plot[0]} ({exp_var_pc1} %)",
            'y': f"PC{pc_to_plot[1]} ({exp_var_pc2} %)",
            'color': color
            },
    title="PCoA",
    hover_name=df_metadata_resticted[filename_col],
    template="simple_white"
    )
    fig.update_layout({'width':1000, 'height':650})
    fig.show()

    result = {}
    result['fig'] = fig
    result['dm'] = dm_memo
    result['pcoa'] = pcoa_results
    return result


def plot_pcoa_3d(memo_matrix, df_metadata, filename_col, color, metric = 'braycurtis', norm = False, scaling = False, pc_to_plot = [1,2,3]):
    '''
    Compute distance matrix and perform PCoA on it from a given MEMO matrix
    Output 3D score plot, distance matrix and skbio.pcoa 

    plot_pcoa_3d(memo_matrix, df_metadata, filename_col, color, metric = 'braycurtis', norm = False, scaling = False, pc_to_plot = [1,2,3])
    Args:
        memo_matrix
        df_metadata
        filename_col
        color
        metric
        norm
        scaling
        pc_to_plot
    ''' 
    df_metadata_resticted = df_metadata[df_metadata[filename_col].isin(list(memo_matrix.index))]
    memo_matrix = memo_matrix[memo_matrix.index.isin(list(df_metadata_resticted.Filename))].reindex(list(df_metadata_resticted.Filename))
    if norm == True:
        memo_matrix = memo_matrix.div(memo_matrix.sum(axis=1), axis=0)
    if scaling == True:
        memo_matrix = memo_matrix.to_numpy()
        memo_matrix = np.where(memo_matrix== 0, 0.1, memo_matrix)         
        memo_matrix = np.log10(memo_matrix) # Log scale (base-10)
        memo_matrix = np.where(memo_matrix== -1, 0, memo_matrix)         
        memo_matrix = cb.utils.scale(memo_matrix, method='pareto')

    dm_memo = sp.spatial.distance.pdist(memo_matrix, metric)
    pcoa_results = pcoa(dm_memo)

    x = pcoa_results.samples[f'PC{pc_to_plot[0]}']
    y = pcoa_results.samples[f'PC{pc_to_plot[1]}']
    z = pcoa_results.samples[f'PC{pc_to_plot[2]}']

    exp_var_pc1 = round(100*pcoa_results.proportion_explained[pc_to_plot[0] - 1 ], 1)
    exp_var_pc2 = round(100*pcoa_results.proportion_explained[pc_to_plot[1] - 1 ], 1)
    exp_var_pc3 = round(100*pcoa_results.proportion_explained[pc_to_plot[2] - 1 ], 1)

    fig = px.scatter_3d(x=x, y=y, z=z, color=df_metadata_resticted[color],
    labels={'x': f"PC{pc_to_plot[0]} ({exp_var_pc1} %)",
            'y': f"PC{pc_to_plot[1]} ({exp_var_pc2} %)",
            'z': f"PC{pc_to_plot[2]} ({exp_var_pc3} %)",
            'color': color
            },
    title="PCoA",
    hover_name=df_metadata_resticted[filename_col],
    template="simple_white"
    )
    fig.update_layout({'width':1000, 'height':650})
    fig.show()

    result = {}
    result['fig'] = fig
    result['dm'] = dm_memo
    result['pcoa'] = pcoa_results
    return result