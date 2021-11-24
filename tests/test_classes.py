import os
import numpy as np
import pytest
import memo_ms as memo


PATH_ROOT = os.path.dirname((__file__))
PATH_TEST_RESOURCES = os.path.join(PATH_ROOT, 'test_data')


def test_spectra_documents():
    filename = os.path.join(PATH_TEST_RESOURCES, "test_spectra.mgf")
    spectra = memo.SpectraDocuments(filename)

    assert len(spectra.spectra) == 3, "Expected 3 spectra"
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


def test_spectra_documents_changed_decimals():
    filename = os.path.join(PATH_TEST_RESOURCES, "test_spectra.mgf")
    spectra = memo.SpectraDocuments(filename,
                                    n_decimals=3)
    assert len(spectra.spectra) == 3, "Expected 3 spectra"
    assert spectra.n_decimals == 3, "Expected different parameter"
    assert spectra.document.documents[0][0] == "peak@71.049", \
        "Expected differnt word in document"
    assert spectra.document.documents[2][-1] == "peak@445.114", \
        "Expected differnt word in document"


def test_spectra_documents_no_losses():
    filename = os.path.join(PATH_TEST_RESOURCES, "test_spectra.mgf")
    spectra = memo.SpectraDocuments(filename,
                                    losses_to=0)
    assert len(spectra.spectra) == 3, "Expected 3 spectra"
    assert spectra.n_decimals == 2, "Expected different parameter"
    assert spectra.document.documents[0][0] == "peak@71.05", \
        "Expected differnt word in document"
    assert spectra.document.documents[1][-1] == "peak@278.19", \
        "Expected differnt word in document"
    assert "loss" not in [x.split("@")[0] for x in spectra.document.documents[1]], \
        "Expected no losses."


def test_feature_table():
    filename = os.path.join(PATH_TEST_RESOURCES, "test_table.csv")
    table = memo.FeatureTable(filename)
    assert table.quant_table.shape == (198, 3), "Expected different table shape"
    assert table.quant_table.index[0] == "QEC18_Blank_resusp_20181227024429.mzML", \
        "Expected different filename in table index"
    expected_first_row = np.array([8.73952054e+08, 1.48157905e+08, 9.83701048e+07])
    np.testing.assert_almost_equal(table.quant_table.to_numpy()[0, :],
                                   expected_first_row, decimal=0)


def test_memo_container_exceptions():
    container = memo.MemoContainer()
    with pytest.raises(ValueError, match=r"featuretable argument missing"):
        container.memo_from_aligned_samples(None, None)
    with pytest.raises(ValueError, match=r"spectradocuments argument missing"):
        container.memo_from_aligned_samples("something", None)
    with pytest.raises(TypeError, match=r"featuretable argument must be of type FeatureTable"):
        container.memo_from_aligned_samples("something", "something")

    filename_table = os.path.join(PATH_TEST_RESOURCES, "test_table.csv")
    table = memo.FeatureTable(filename_table)
    with pytest.raises(TypeError, match=r"spectradocuments argument must be of type SpectraDocuments"):
        container.memo_from_aligned_samples(table, "something")


def test_memo_container():
    container = memo.MemoContainer()
    filename_table = os.path.join(PATH_TEST_RESOURCES, "test_table.csv")
    filename_spectra = os.path.join(PATH_TEST_RESOURCES, "test_spectra.mgf")
    spectra = memo.SpectraDocuments(filename_spectra)
    table = memo.FeatureTable(filename_table)
    container.memo_from_aligned_samples(table, spectra)
    # TODO: add usefull tests -> what is expected for container.memo_matrix etc.