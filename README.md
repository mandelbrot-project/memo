# memo

**M**s2 bas**E**d sa**M**ple vect**O**rization (**MEMO**) package

## Description

MEMO is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their consituents.

The occurence of MS2 Peaks and Neutral Losses in each sample is counted and used to generate an *MS2 fingerprint* of the sample. These fingerprints can in a second stage be aligned to compare different samples. Once obtained, different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used. 

MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers technology (qToF vs QE).

### Small preview of the results on the Qemistree Evaluation Dataset:
Samples colored according to their content
![plot](./pcoa_tuto_contains.png)

Samples colored according to their method of acquisition
![plot](./pcoa_tuto_method.png)


MEMO is built on matchms and spec2vec packages for handling the MS2 spectra and convert them into documents. Huge thanks to them for the amazing work done with these packages! See https://github.com/matchms/matchms for matchms, and https://github.com/iomega/spec2vec for spec2vec. 

### To install it:

First make sure to have anaconda3 installed: https://www.anaconda.com/products/individual

#### A) Clone and install locally
A.1. First clone the repository using git clone in command line:
```
git clone <ssh_key or https>
```
A.2. Create a new conda environment to avoid clashes:
```
conda create --name memo python
conda activate memo
```

A.3. Install the package locally using pip:
```
pip install .
```
#### B) Using pip

B.1. Create a new conda environment to avoid clashes:
```
conda create --name memo python
conda activate memo
```
B.2. Install with pip from test.pypi (experimental)
```
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ memo-ms
```

If you have an error, try using
```
conda install -c conda-forge scikit-bio
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ memo-ms
```

You can clone the repository to get the demo spectra and quant table files!

#### Enjoy!

Once installed, try it using the tutorial jupyter notebook.

Please add feedback to the issues section. Thanks !
