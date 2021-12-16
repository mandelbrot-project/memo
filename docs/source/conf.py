# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../memo_ms/'))

import memo_ms

# -- Project information -----------------------------------------------------

project = 'memo'
copyright = '2021, Arnaud Gaudry'
author = 'Arnaud Gaudry'

# The full version, including alpha/beta/rc tags
release = '0.1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']




# import matchms

# # -- Project information -----------------------------------------------------

# project = "matchms"
# copyright = "2020, Netherlands eScience Center"
# author = "Netherlands eScience Center"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "sphinxcontrib.apidoc",
    "sphinx.ext.napoleon",
]

apidoc_module_dir = "../../memo_ms/"
apidoc_output_dir = "./api"
apidoc_excluded_paths = ["tests", "readthedocs"]
apidoc_separate_modules = True
apidoc_module_first = True
autodoc_default_options = {
    'special-members': '__init__,__call__',
    'inherited-members': True,
}
autodoc_mock_imports = [
    'rdkit',
]
# Hide undocumented member by excluding default undoc-members option
os.environ["SPHINX_APIDOC_OPTIONS"] = "members,show-inheritance"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "docs/conf.rst"]


# # -- Options for HTML output -------------------------------------------------

# # The theme to use for HTML and HTML Help pages.  See the documentation for
# # a list of builtin themes.
# #
# html_theme = "alabaster"

# html_theme_options = {
#     "logo": "matchms.png",
#     "github_user": "matchms",
#     "github_repo": "matchms",
#     "page_width": '1080px',
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Extension configuration -------------------------------------------------

napoleon_google_docstring = False

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for intersphinx extension ----------------------------------------------

intersphinx_mapping = {
    "gensim": ("https://radimrehurek.com/gensim", None),
    "https://docs.python.org/3": None,
    "matplotlib": ("https://matplotlib.org", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
    "pyteomics": ("https://pyteomics.readthedocs.io/en/latest/", None),
    "rdkit": ("http://rdkit.org/docs", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None)
}