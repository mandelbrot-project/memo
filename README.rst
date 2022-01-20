|GitHub Workflow Status| |GitHub| |PyPI| |Docs|

MEMO
===============
.. image:: https://github.com/mandelbrot-project/memo_publication_examples/blob/main/docs/memo_logo.jpg
   :width: 200 px
   :align: right

Description
-----------------

**M**\ s2 bas\ **E**\ d sa\ **M**\ ple vect\ **O**\ rization (**MEMO**)
is a method allowing a Retention Time (RT) agnostic alignment of
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

Documentation
------------------
For documentation, see our `readthedocs`_. Different examples of application and comparison to other MS/MS based metrics are available `here`_ and the corresponding notebooks are available on `GitHub`_.

Publication
-----------

If you use MEMO, please cite the following papers:
   - MEMO preprint - MEMO: Mass Spectrometry-based Sample Vectorization to Explore Chemodiverse Datasets Arnaud Gaudry, Florian Huber, Louis-Felix Nothias, Sylvian Cretton, Marcel Kaiser, Jean-Luc Wolfender, Pierre-Marie Allard bioRxiv 2021.12.24.474089; doi: https://doi.org/10.1101/2021.12.24.474089
   - Huber, Florian, Stefan Verhoeven, Christiaan Meijer, Hanno Spreeuw, Efraín Castilla, Cunliang Geng, Justin van der Hooft, et al. 2020. “Matchms - Processing and Similarity Evaluation of Mass Spectrometry Data.” Journal of Open Source Software 5 (52): 2411. https://doi.org/10.21105/joss.02411 
   - Huber, Florian, Lars Ridder, Stefan Verhoeven, Jurriaan H. Spaaks, Faruk Diblen, Simon Rogers, and Justin J. J. van der Hooft. 2021. “Spec2Vec: Improved Mass Spectral Similarity Scoring through Learning of Structural Relationships.” PLoS Computational Biology 17 (2): e1008724. https://doi.org/10.1371/journal.pcbi.1008724

Installation :
-------------------------

First make sure to have `anaconda`_ installed.

A) Recommended: using pip install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A.1. Create a new conda environment to avoid clashes:

.. code-block:: console

   conda create --name memo python=3.8
   conda activate memo

A.2. Install with pip:

.. code-block:: console

   pip install numpy
   pip install memo-ms

If you have an error, try installing scikit-bio from conda-forge (available for Mac and Linux users) or pip (for Windows users) before
installing the package with pip. For Windows users, you will need to install C++ build tools (download here: https://visualstudio.microsoft.com/visual-cpp-build-tools/, see this answer for help https://stackoverflow.com/a/50210015):

.. code-block:: console

   conda install -c conda-forge scikit-bio
   # or for Windows user
   pip install scikit-bio
   pip install memo-ms

You can clone the repository to get the demo spectra and quant table
files and test the package using the Tutorial notebook!

NB: If you have this error when loading the memo package:

.. code-block:: console

   ValueError: numpy.ndarray size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject

Uninstall and reinstall scikit-bio with no dependencies using this command:

.. code-block:: console

   pip uninstall scikit-bio
   pip install scikit-bio --no-cache-dir --no-binary :all:


B) Alternatively: clone and install locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

B.1. First clone the repository using git clone in command line:

.. code-block:: console

   git clone https://github.com/mandelbrot-project/memo.git # or ssh

B.2. Create a new conda environment to avoid clashes:

.. code-block:: console

   conda create --name memo python=3.8
   conda activate memo

B.3. Install the package locally using pip

.. code-block:: console

   pip install .
   
Run example notebook
-----------------------------------

It is located in the `tutorial folder`_

You can also find a list of notebook to reproduce results of the MEMO paper. The repo is over there https://github.com/mandelbrot-project/memo_publication_examples
   

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

License
-----------

MEMO is licensed under the GNU General Public License v3.0. Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

.. _Qemistree Evaluation Dataset: https://www.nature.com/articles/s41589-020-00677-3
.. _matchms: https://github.com/matchms/matchms
.. _spec2vec: https://github.com/iomega/spec2vec
.. _here: https://mandelbrot-project.github.io/memo_publication_examples/
.. _GitHub: https://github.com/mandelbrot-project/memo_publication_examples
.. _readthedocs: https://memo-docs.readthedocs.io/en/latest/index.html#
.. _anaconda: https://www.anaconda.com/products/individual
.. _`tutorial folder`: https://github.com/mandelbrot-project/memo/blob/b14409a545aa499992b92c3eb9445405ceba9a78/tutorial/tutorial_memo.ipynb


.. |GitHub Workflow Status| image:: https://img.shields.io/github/workflow/status/mandelbrot-project/memo/CI%20Build
   :target: https://github.com/mandelbrot-project/memo/actions
.. |GitHub| image:: https://img.shields.io/github/license/mandelbrot-project/memo?color=blue
.. |PyPI| image:: https://img.shields.io/pypi/v/memo_ms?color=blue)
   :target: https://pypi.org/project/memo-ms/
.. |Docs| image:: https://readthedocs.org/projects/memo-docs/badge/?version=stable
   :target: https://memo-docs.readthedocs.io/en/stable/?badge=stable
   :alt: Documentation Status
