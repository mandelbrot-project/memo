import pandas as pd

def import_mzmine2_quant_table(path):
    '''
    Read and clean a MzMine2 quant table.
    Returns a pd.DataFrame with features' area in samples.
    '''
    quant_table = pd.read_csv(path, sep=',')
    quant_table.set_index('row ID', inplace=True)
    quant_table = quant_table.filter(like='Peak area', axis=1)
    quant_table.rename(columns = lambda x: x.replace(' Peak area', ''), inplace=True)
    return quant_table