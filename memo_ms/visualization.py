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


def plot_pcoa_2d(
    matrix, df_metadata, filename_col, group_col,
    metric = 'braycurtis', norm = False, scaling = False, pc_to_plot = (1, 2)
    ):
    """ Simple 2D PCoA plot of a MEMO matrix / Feature table using Plotly

    Args:
        matrix (DataFrame): A Table in the MemoMatrix.memo_matrix or FeatureTable.feature_table format
        df_metadata (DataFrame): Metadata of the MEMO matrix samples
        filename_col (str): Column name in df_metadata to match memo_matrix index
        group_col (str): Column name in df_metadata to use as groups for plotting
        metric (str, optional): Distance metric to use, see
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html. Defaults to 'braycurtis'.
        norm (bool, optional): Apply samples normalization. Defaults to False.
        scaling (bool, optional): Apply pareto scaling to MEMO matrix columns. Defaults to False.
        pc_to_plot (list of int, optional): PCs to plot. Defaults to [1,2].

    Returns:
        None
    """
    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-locals
    df_metadata_resticted = df_metadata[df_metadata[filename_col].isin(list(matrix.index))]
    matrix = matrix[matrix.index.isin(list(df_metadata_resticted[filename_col]))].reindex(list(df_metadata_resticted[filename_col]))
    if norm is True:
        matrix = matrix.div(matrix.sum(axis=1), axis=0)
    if scaling is True:
        matrix = matrix.to_numpy()
        matrix = np.log10(matrix, out=np.zeros_like(matrix), where=(matrix!=0)) # Log scale (base-10)
        matrix = cb.utils.scale(matrix, method='pareto')

    dm_memo = sp.spatial.distance.pdist(matrix, metric)
    pcoa_results = pcoa(dm_memo)

    x = pcoa_results.samples[f'PC{pc_to_plot[0]}']
    y = pcoa_results.samples[f'PC{pc_to_plot[1]}']


    exp_var_pc1 = round(100*pcoa_results.proportion_explained[pc_to_plot[0] - 1 ], 1)
    exp_var_pc2 = round(100*pcoa_results.proportion_explained[pc_to_plot[1] - 1 ], 1)

    fig = px.scatter(x=x, y=y, color=df_metadata_resticted[group_col],
        labels={'x': f"PC{pc_to_plot[0]} ({exp_var_pc1} %)",
                'y': f"PC{pc_to_plot[1]} ({exp_var_pc2} %)",
                'color': group_col
                },
        title="2D PCoA",
        hover_name=df_metadata_resticted[filename_col],
        template="simple_white"
    )
    fig.update_layout({'width':1000, 'height':650})
    fig.show()


def plot_pcoa_3d(
    matrix, df_metadata, filename_col, group_col,
    metric = 'braycurtis', norm = False, scaling = False, pc_to_plot = (1, 2, 3)
    ):
    """ Simple 2D PCoA plot of a MEMO matrix / Feature table using Plotly

    Args:
        matrix (DataFrame): A Table in the MemoMatrix.memo_matrix or FeatureTable.feature_table format
        df_metadata (DataFrame): Metadata of the MEMO matrix samples
        filename_col (str): Column name in df_metadata to match memo_matrix index
        group_col (str): Column name in df_metadata to use as groups for plotting
        metric (str, optional): Distance metric to use, see
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html. Defaults to 'braycurtis'.
        norm (bool, optional): Apply samples normalization. Defaults to False.
        scaling (bool, optional): Apply pareto scaling to MEMO matrix columns. Defaults to False.
        pc_to_plot (list of int, optional): PCs to plot. Defaults to [1,2,3].

    Returns:
        None
    """
    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-locals
    df_metadata_resticted = df_metadata[df_metadata[filename_col].isin(list(matrix.index))]
    matrix = matrix[matrix.index.isin(list(df_metadata_resticted[filename_col]))].reindex(list(df_metadata_resticted[filename_col]))
    if norm is True:
        matrix = matrix.div(matrix.sum(axis=1), axis=0)
    if scaling is True:
        matrix = matrix.to_numpy()
        matrix = np.log10(matrix, out=np.zeros_like(matrix), where=(matrix!=0)) # Log scale (base-10)
        matrix = cb.utils.scale(matrix, method='pareto')

    dm_memo = sp.spatial.distance.pdist(matrix, metric)
    pcoa_results = pcoa(dm_memo)

    x = pcoa_results.samples[f'PC{pc_to_plot[0]}']
    y = pcoa_results.samples[f'PC{pc_to_plot[1]}']
    z = pcoa_results.samples[f'PC{pc_to_plot[2]}']

    exp_var_pc1 = round(100*pcoa_results.proportion_explained[pc_to_plot[0] - 1 ], 1)
    exp_var_pc2 = round(100*pcoa_results.proportion_explained[pc_to_plot[1] - 1 ], 1)
    exp_var_pc3 = round(100*pcoa_results.proportion_explained[pc_to_plot[2] - 1 ], 1)

    fig = px.scatter_3d(x=x, y=y, z=z, color=df_metadata_resticted[group_col],
        labels={'x': f"PC{pc_to_plot[0]} ({exp_var_pc1} %)",
                'y': f"PC{pc_to_plot[1]} ({exp_var_pc2} %)",
                'z': f"PC{pc_to_plot[2]} ({exp_var_pc3} %)",
                'color': group_col
                },
        title="3D PCoA",
        hover_name=df_metadata_resticted[filename_col],
        template="simple_white"
    )
    fig.update_layout({'width':1000, 'height':650})
    fig.show()


def plot_hca(
    matrix, df_metadata, filename_col, group_col,
    plotly_discrete_cm = px.colors.qualitative.Plotly,
    linkage_method = 'ward', linkage_metric = 'euclidean',
    norm = False, scaling = False):
    """Simple HCA plot of a MEMO matrix / Feature table using matplotlib

    Args:
        matrix (DataFrame): A Table in the MemoMatrix.memo_matrix or FeatureTable.feature_table format
        df_metadata (DataFrame): Metadata of the MEMO matrix samples
        filename_col (str): Column name in df_metadata to match memo_matrix index
        group_col (str): Column name in df_metadata to use as groups for plotting
        plotly_discrete_cm ([type], optional): Plotly discrete colormap to use for groups. Defaults to px.colors.qualitative.Plotly.
        linkage_method (str, optional): Linkage method to use. Defaults to 'ward'.
        linkage_metric (str, optional): Linkage metric to use. Defaults to 'euclidean'.
        norm (bool, optional): Apply samples normalization. Defaults to False.
        scaling (bool, optional): Apply pareto scaling to MEMO matrix columns. Defaults to False.

    Returns:
        None
    """
    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-locals
    #pylint: disable=dangerous-default-value
    df_metadata_resticted = df_metadata[df_metadata[filename_col].isin(list(matrix.index))]
    matrix = matrix[matrix.index.isin(list(df_metadata_resticted[filename_col]))].reindex(list(df_metadata_resticted[filename_col]))
    if norm is True:
        matrix = matrix.div(matrix.sum(axis=1), axis=0)
    if scaling is True:
        matrix = matrix.to_numpy()
        matrix = np.log10(matrix, out=np.zeros_like(matrix), where=(matrix!=0)) # Log scale (base-10)
        matrix = cb.utils.scale(matrix, method='pareto')

    groups = df_metadata_resticted[group_col].unique()
    colors_list = plotly_discrete_cm
    dic_col = dict(zip(groups, cycle(colors_list)))

    Z = linkage(matrix, method=linkage_method, metric=linkage_metric)

    plt.figure(figsize=(12, 8), dpi=80)

    dendrogram(
        Z, labels =df_metadata_resticted[group_col].to_list(),
        leaf_rotation=0,
        orientation='left'
        )
    xlbls = plt.gca().get_yticklabels()
    for lbl in xlbls:
        lbl.set_color(dic_col[lbl.get_text()])

    plt.show()


def plot_heatmap(
    matrix, df_metadata, filename_col, group_col,
    plotly_discrete_cm = px.colors.qualitative.Plotly,
    linkage_method = 'ward', linkage_metric = 'euclidean',
    heatmap_metric = 'braycurtis', norm = False, scaling = False):
    """HCA and heatmap plot of a MEMO matrix / Feature table using Plotly

    Args:
        matrix (DataFrame): A Table in the MemoMatrix.memo_matrix or FeatureTable.feature_table format
        df_metadata (DataFrame): Metadata of the MEMO matrix samples
        filename_col (str): Column name in df_metadata to match memo_matrix index
        group_col (str): Column name in df_metadata to use as groups for plotting
        plotly_discrete_cm ([type], optional): Plotly discrete colormap to use for groups. Defaults to px.colors.qualitative.Plotly.
        linkage_method (str, optional): Linkage method to use. Defaults to 'ward'.
        linkage_metric (str, optional): Linkage metric to use. Defaults to 'euclidean'.
        heatmap_metric (str, optional): Distance metric to use for heatmap. Defaults to 'braycurtis'.
        norm (bool, optional): Apply samples normalization. Defaults to False.
        scaling (bool, optional): Apply pareto scaling to MEMO matrix columns. Defaults to False.

    Returns:
        None
    """
    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-locals
    #pylint: disable=dangerous-default-value
    df_metadata_resticted = df_metadata[df_metadata[filename_col].isin(list(matrix.index))]
    matrix = matrix[matrix.index.isin(list(df_metadata_resticted[filename_col]))].reindex(list(df_metadata_resticted[filename_col]))
    if norm is True:
        matrix = matrix.div(matrix.sum(axis=1), axis=0)
    if scaling is True:
        matrix = matrix.to_numpy()
        matrix = np.log10(matrix, out=np.zeros_like(matrix), where=(matrix!=0)) # Log scale (base-10)
        matrix = cb.utils.scale(matrix, method='pareto')

    dm_memo = sp.spatial.distance.pdist(matrix, heatmap_metric)

    fig = ff.create_dendrogram(matrix, orientation='bottom', labels= df_metadata_resticted[group_col].to_list(),
    linkagefun=lambda x: linkage(x, method=linkage_method, metric = linkage_metric)
    )
    for i in range(len(fig['data'])):
        fig['data'][i]['yaxis'] = 'y2'

    # Create Side Dendrogram
    dendro_side = ff.create_dendrogram(matrix, orientation='right',
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
    groups = df_metadata_resticted[group_col].unique()
    colors_list = plotly_discrete_cm
    dic_col = dict(zip(groups, cycle(colors_list)))
    scats = []
    for group in groups:
        scat_group = df_meta_reindex[df_meta_reindex[group_col] == group]
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
    # Edit yaxis3
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
