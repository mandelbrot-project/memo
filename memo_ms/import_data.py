import pandas as pd
from matchms.importing import load_from_mgf
from matchms.filtering import add_precursor_mz
from matchms.filtering import add_losses
from matchms.filtering import normalize_intensities
from matchms.filtering import require_minimum_number_of_peaks
from matchms.filtering import select_by_relative_intensity

def load_and_filter_from_mgf(path, min_relative_intensity, max_relative_intensity,
                             loss_mz_from, loss_mz_to, n_required) -> list:
    """Load and filter spectra from mgf file to prepare for MEMO matrix generation

    Returns:
        spectrums (list of matchms.spectrum): a list of matchms.spectrum objects
    """
    #pylint: disable=too-many-arguments
    def apply_filters(spectrum):
        spectrum = add_precursor_mz(spectrum)
        spectrum = normalize_intensities(spectrum)
        spectrum = select_by_relative_intensity(spectrum, intensity_from = min_relative_intensity,
                                                intensity_to = max_relative_intensity)
        spectrum = add_precursor_mz(spectrum)
        spectrum = add_losses(spectrum, loss_mz_from= loss_mz_from, loss_mz_to= loss_mz_to)
        spectrum = require_minimum_number_of_peaks(spectrum, n_required= n_required)
        return spectrum

    spectra_list = [apply_filters(s) for s in load_from_mgf(path)]
    spectra_list = [s for s in spectra_list if s is not None]
    return spectra_list 

def import_mzmine2_quant_table(path) -> pd.DataFrame:
    """Import feature quantification table generated from MzMine 2 and clean it

    Args:
        path (str): Path to feature quantification table

    Returns:
        quant_table (DataFrame): A cleaned MzMine2 feature quantification table
    """
    quant_table = pd.read_csv(path, sep=',')
    quant_table.set_index('row ID', inplace=True)
    quant_table = quant_table.filter(like='Peak area', axis=1)
    quant_table.rename(columns = lambda x: x.replace(' Peak area', ''), inplace=True)
    quant_table = quant_table.transpose()
    quant_table.index.name = 'filename'
    quant_table.columns.name = 'feature_id'
    return quant_table

def import_msdial_quant_table(path) -> pd.DataFrame:
    """Import feature quantification table generated from MS-DIAL and clean it

    Args:
        path (str): Path to feature quantification table

    Returns:
        quant_table (DataFrame): A cleaned MS-DIAL feature quantification table
    """
    quant_table = pd.read_csv(path, sep='\t', index_col=0)
    quant_table = quant_table.drop(quant_table.filter(regex='Unnamed').columns, axis=1)
    quant_table = quant_table[quant_table.index.notnull()]
    quant_table.columns = quant_table.iloc[0]
    quant_table = quant_table.iloc[1: , :]
    quant_table = quant_table.drop(columns=['MS/MS spectrum']).transpose()
    quant_table.index.name = 'filename'
    quant_table.columns.name = 'feature_id'
    return quant_table

def import_xcms_quant_table(path) -> pd.DataFrame:
    """Import feature quantification table generated from XCMS and clean it

    Args:
        path (str): Path to feature quantification table

    Returns:
        quant_table (DataFrame): A cleaned XCMS feature quantification table
    """
    quant_table = pd.read_csv(path, sep='\t', index_col=0)
    ext = quant_table.columns[-1].split(sep='.')[-1]
    quant_table = quant_table.filter(like=ext, axis=1)
    quant_table.index = quant_table.index.str.replace('FT', '').astype(int)
    quant_table = quant_table.transpose().fillna(0)
    quant_table.index.name = 'filename'
    quant_table.columns.name = 'feature_id'
    return quant_table
