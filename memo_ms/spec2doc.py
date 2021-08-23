from spec2vec import SpectrumDocument
import pandas as pd

def spec2doc(spectrums, n_decimals = 2):
    ''' 
    Apply filters to spectra and convert them to words vectors with the number of specified decimals.
    Returns a pd.DataFrame with spectra "documents" and metadata.

    spec2doc(spectrums, n_decimals = 2)
    Args:
        spectrums (matchms.Spectrum) - a list of matchms.Spectrum
        n_decimals (int) - the number of decimal to use for word creation
    '''
    documents = [SpectrumDocument(s, n_decimals=n_decimals) for s in spectrums]
    doc_with_meta = pd.DataFrame(s.metadata for s in spectrums)
    doc_with_meta['documents'] = list(doc.words for doc in documents)
    doc_with_meta.scans = doc_with_meta.scans.astype(int)
    return doc_with_meta