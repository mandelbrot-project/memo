import os
import numpy as np
import memo_ms as memo


PATH_ROOT = os.path.dirname((__file__))
PATH_TEST_RESOURCES = os.path.join(PATH_ROOT, 'test_data')


def test_spectra_documents():
    filename = os.path.join(PATH_TEST_RESOURCES, "test_spectra.mgf")
    spectra = memo.SpectraDocuments(filename)
    
    assert len(spectra.spectra), "Expected 3 spectra"
    assert type(spectra.spectra) == list, "Expected list of spectra"
    assert spectra.min_relative_intensity == 0.01, "Expected different default parameter"
    assert spectra.max_relative_intensity == 1.0, "Expected different default parameter"
    assert spectra.min_peaks_required == 10, "Expected different default parameter"
    assert spectra.n_decimals == 2, "Expected different default parameter"
    assert spectra.document.shape == (3, 6), "Expected different DataFrame shape"
    # Check some of the document table content:
    expected_precursor_mz = [338.342, 278.1905, 702.2131]
    assert spectra.document.precursor_mz.to_list() == expected_precursor_mz, \
        "Expected different precursor m/z values"
    assert spectra.document.documents[0][0] == "peak@71.05", \
        "Expected differnt word in document"
    assert spectra.document.documents[1][-1] == "loss@194.11", \
        "Expected differnt word in document"
    assert spectra.document.documents[2][-1] == "peak@445.11", \
        "Expected differnt word in document"


def test_feature_table():
    filename = os.path.join(PATH_TEST_RESOURCES, "test_table.csv")
    table = memo.FeatureTable(filename)
    assert table.quant_table.shape == (198, 3), "Expected different table shape"
    assert table.quant_table.index[0] == "QEC18_Blank_resusp_20181227024429.mzML", \
        "Expected different filename in table index"
    expected_first_row = np.array([8.73952054e+08, 1.48157905e+08, 9.83701048e+07])
    np.testing.assert_almost_equal(table.quant_table.to_numpy()[0, :],
                                   expected_first_row, decimal=0)