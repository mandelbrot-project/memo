|GitHub Workflow Status| |GitHub| |PyPI|

MEMO
===============

**M**\ s2 bas\ **E**\ d sa\ **M**\ ple vect\ **O**\ rization (**MEMO**)
package

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
technology (Maxiis qToF vs Q-Exactive).

MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling
the MS2 spectra and convert them into documents. Huge thanks to them for
the amazing work done with these packages!

Examples
------------------

Different examples of application and comparison to other MS/MS based metrics are avalable `here`_ and notebooks are available on `GitHub`_

Publication
-----------

To add

To install it:
-------------------------

First make sure to have `anaconda`_ installed.

A) Using pip install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A.1. Create a new conda environment to avoid clashes:

.. code-block:: console

   conda create --name memo python=3.8
   conda activate memo

A.2. Install with pip:

.. code-block:: console

   pip install numpy
   pip install memo-ms

If you have an error, try insstalling scikit-bio from conda-forge before
installing the package with pip:

.. code-block:: console

   conda install -c conda-forge scikit-bio
   pip install memo-ms

You can clone the repository to get the demo spectra and quant table
files!

B) Clone and install locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

B.1. First clone the repository using git clone in command line:

.. code-block:: console

   git clone <ssh_key or https>

B.2. Create a new conda environment to avoid clashes:

.. code-block:: console

   conda create --name memo python
   conda activate memo

B.3. Install the package locally using pip

.. code-block:: console

   pip install .
   
C) Test it using the Tutorial notebook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Documentation for developers
----------------------------------

Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create an environment with

.. code-block:: console

   git clone https://github.com/mandelbrot-project/memo.git
   cd memo
   conda create --name memo-dev python=3.8
   conda activate memo-dev

Then install dependencies and memo:

.. code-block:: console

   python -m pip install --upgrade pip
   pip install numpy
   pip install --editable .[dev]
   # pip install -e .'[dev]' (on mac)

Run tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Memo tests can be run by:

.. code-block:: console

   pytest

And the code linter with

.. code-block:: console

   prospector

.. _Qemistree Evaluation Dataset: https://www.nature.com/articles/s41589-020-00677-3
.. _matchms: https://github.com/matchms/matchms
.. _spec2vec: https://github.com/iomega/spec2vec
.. _here: https://mandelbrot-project.github.io/memo_publication_examples/
.. _GitHub: https://github.com/mandelbrot-project/memo_publication_examples
.. _anaconda: https://www.anaconda.com/products/individual

.. |GitHub Workflow Status| image:: https://img.shields.io/github/workflow/status/mandelbrot-project/memo/CI%20Build
.. |GitHub| image:: https://img.shields.io/github/license/mandelbrot-project/memo?color=blue
.. |PyPI| image:: https://img.shields.io/pypi/v/memo_ms?color=blue)
   :target: https://pypi.org/project/memo-ms/
  
