from matchms.importing import load_from_mgf
from matchms.filtering import add_losses
from matchms.filtering import normalize_intensities
from matchms.filtering import require_minimum_number_of_peaks
from matchms.filtering import select_by_relative_intensity


def load_and_filter_from_mgf(
    path_to_spectra,
    min_relative_intensity = 0.01, max_relative_intensity = 1.00,
    min_peaks_required = 10,
    losses_from = 10, losses_to = 200):
    """
    Import spectra from mgf an apply optionnal minimal filtering, and detect losses in spectra
    Returns a list of matchms.Spectrum 
    """
    def apply_filters(spectrum):
        spectrum = normalize_intensities(spectrum)
        spectrum = select_by_relative_intensity(spectrum, intensity_from = min_relative_intensity, intensity_to = max_relative_intensity)
        spectrum = add_losses(spectrum, loss_mz_from=losses_from, loss_mz_to=losses_to)
        spectrum = require_minimum_number_of_peaks(spectrum, n_required=min_peaks_required)
        return spectrum

    spectrums = [apply_filters(s) for s in load_from_mgf(path_to_spectra)]
    spectrums = [s for s in spectrums if s is not None]
    return spectrums
    