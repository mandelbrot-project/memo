.. memo documentation master file, created by
   sphinx-quickstart on Thu Dec 16 21:33:56 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to memo's documentation!
================================

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   API <api/memo_ms.rst>

Description
-----------------

MEMO is a method allowing a Retention Time (RT) agnostic alignment of
metabolomics samples using the fragmentation spectra (MS2) of their
consituents. The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted
and used to generate an *MS2 fingerprint* of the sample. These
fingerprints can in a second stage be aligned to compare different
samples. Once obtained, different filtering (remove peaks/losses from
blanks for example) and visualization techniques (MDS/PCoA, TMAP,
Heatmap, ...) can be used. MEMO suits particularly well to compare chemodiverse samples, ie with a
poor features overlap, or to compare samples with a strong RT shift,
acquired using different LC methods or even different mass spectrometers
technology (Maxiis Q-ToF vs Q-Exactive).

MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling
the MS2 spectra and convert them into documents. Huge thanks to them for
the amazing work done with these packages!

To install it:
-------------------------

First make sure to have `anaconda`_ installed.

1. Create a new conda environment to avoid clashes:

.. code-block:: console

   conda create --name memo python=3.8
   conda activate memo

2. Install with pip:

.. code-block:: console

   pip install numpy
   pip install memo-ms

If you have an error, try insstalling scikit-bio from conda-forge before
installing the package with pip:

.. code-block:: console

   conda install -c conda-forge scikit-bio
   pip install memo-ms

You can clone the Github package repository to get the demo files and the tutorial!

Examples
------------------

Different examples of application and comparison to other MS/MS based metrics are available `here`_ and the corresponding notebooks are available on `GitHub`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _matchms: https://github.com/matchms/matchms
.. _spec2vec: https://github.com/iomega/spec2vec
.. _here: https://mandelbrot-project.github.io/memo_publication_examples/
.. _GitHub: https://github.com/mandelbrot-project/memo_publication_examples
.. _anaconda: https://www.anaconda.com/products/individual
