import pandas as pd
import numpy as np
import scipy as sp
from itertools import cycle
from skbio.stats.ordination import pcoa
import cimcb_lite as cb
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

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


def plot_hca(
    memo_matrix, df_metadata, filename_col, label_col, plotly_discrete_cm = px.colors.qualitative.Plotly,
    linkage_method = 'ward', linkage_metric = 'euclidean',
    norm = False, scaling = False):
    '''
    Compute distance matrix and perform PCoA on it from a given MEMO matrix
    Output 3D score plot, distance matrix and skbio.pcoa 

    plot_pcoa_3d(memo_matrix, df_metadata, filename_col, color, metric = 'braycurtis', norm = False, scaling = False, pc_to_plot = [1,2,3])
    Args:
        memo_matrix
        df_metadata
        filename_col
        label_col
        plotly_discrete_cm
        metric
        norm
        scaling
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

    groups = df_metadata_resticted[label_col].unique()
    colors_list = plotly_discrete_cm
    dic_col = dict(zip(groups, cycle(colors_list)))

    Z = linkage(memo_matrix, method=linkage_method, metric=linkage_metric)
    
    fig = plt.figure(figsize=(12, 8), dpi=80)

    dendrogram(
        Z, labels =df_metadata_resticted[label_col].to_list(),
        leaf_rotation=0, 
        orientation='left'
        )
    xlbls = plt.gca().get_yticklabels()
    for lbl in xlbls:
        lbl.set_color(dic_col[lbl.get_text()])

    plt.show()

def plot_heatmap(
    memo_matrix, df_metadata, filename_col, label_col, plotly_discrete_cm = px.colors.qualitative.Plotly,
    linkage_method = 'ward', linkage_metric = 'euclidean',
    heatmap_metric = 'braycurtis', norm = False, scaling = False):
    '''
    Compute distance matrix and perform PCoA on it from a given MEMO matrix
    Output 3D score plot, distance matrix and skbio.pcoa 

    plot_pcoa_3d(memo_matrix, df_metadata, filename_col, color, metric = 'braycurtis', norm = False, scaling = False, pc_to_plot = [1,2,3])
    Args:
        memo_matrix
        df_metadata
        filename_col
        label_col
        plotly_discrete_cm
        metric
        norm
        scaling
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

    dm_memo = sp.spatial.distance.pdist(memo_matrix, heatmap_metric)

    fig = ff.create_dendrogram(memo_matrix, orientation='bottom', labels= df_metadata_resticted[label_col].to_list(), 
    linkagefun=lambda x: linkage(x, method=linkage_method, metric = linkage_metric)
    )
    for i in range(len(fig['data'])):
        fig['data'][i]['yaxis'] = 'y2'

    # Create Side Dendrogram
    dendro_side = ff.create_dendrogram(memo_matrix, orientation='right',
    linkagefun=lambda x: linkage(x, method=linkage_method, metric = linkage_metric), 
    )
    for i in range(len(dendro_side['data'])):
        dendro_side['data'][i]['xaxis'] = 'x2'

    # Add Side Dendrogram Data to Figure
    for data in dendro_side['data']:
        fig.add_trace(data)

    fig.update_layout(plot_bgcolor  ='rgba(0,0,0,0)')

    # Create Heatmap
    dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
    dendro_leaves = list(map(int, dendro_leaves))
    heat_data = sp.spatial.distance.squareform(dm_memo)
    heat_data = heat_data[dendro_leaves,:]
    heat_data = heat_data[:,dendro_leaves]

    heatmap = [
        go.Heatmap(
            x = dendro_leaves,
            y = dendro_leaves,
            z = heat_data,
            colorscale = 'YlOrRd',
            colorbar=dict(
                title="Distance",
                len= 0.4,
                y= 0.2,
                ypad = 5
            ),
            reversescale = True,
        )
    ]

    heatmap[0]['x'] = fig['layout']['xaxis']['tickvals']
    heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

    # Add Heatmap Data to Figure
    for data in heatmap:
        fig.update_layout({'showlegend':False})
        fig.add_trace(data)

    # Create and add scatter plot for categories
    df_meta_reindex = df_metadata_resticted.reset_index()
    df_meta_reindex = df_meta_reindex.reindex(dendro_leaves)
    df_meta_reindex['x'] = heatmap[0]['x']
    df_meta_reindex['y'] = 1
    groups = df_metadata_resticted[label_col].unique()
    colors_list = plotly_discrete_cm
    dic_col = dict(zip(groups, cycle(colors_list)))
    scats = []
    i_color = 0
    for group in groups:
        scat_group = df_meta_reindex[df_meta_reindex[label_col] == group]
        scat_group = go.Scatter(
            x=scat_group['x'], y=scat_group['y'],
            name=group, marker_color = dic_col[group],
            mode='markers', xaxis= 'x', yaxis = 'y3')
        scats.append(scat_group)
    fig.add_traces(scats)

    # Edit Layout
    fig.update_layout({'width':1200, 'height':800,'hovermode': 'closest', 'showlegend':True})
    fig.update_layout(title_text="Heatmap",
                    title_font_size=15,
                    title_x=0.5)
    fig.update_layout(paper_bgcolor ='rgb(255,255,255)')

    # Edit xaxis
    fig.update_layout(xaxis={'domain': [.15, 1],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'ticks':""}
                                    )
    # Edit xaxis2
    fig.update_layout(xaxis2={'domain': [0, .14],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'showticklabels': False,
                                    'ticks':""})

    # Edit yaxis
    fig.update_layout(yaxis={'domain': [0, .87],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'showticklabels': False,
                                    'ticks': ""
                            })
    # Edit yaxis2
    fig.update_layout(yaxis2={'domain':[0.89, 1],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'showticklabels': False,
                                    'ticks':""})

    fig.update_layout(yaxis3={'domain':[0.84, 0.90],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'showticklabels': False,
                                    'ticks':""})
        
    labels_to_show_in_legend = groups

    for trace in fig['data']: 
        if (not trace['name'] in labels_to_show_in_legend):
            trace['showlegend'] = False

    fig.update_layout(legend=dict(
        orientation="v",
        y = 1,
        x = 1
    ))

    fig.update_xaxes(tickangle=45)
    fig.show()
    
    result = {}
    result['fig'] = fig
    
    return result
