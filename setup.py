import os
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(here, "memo_ms", "__version__.py")) as f:
    exec(f.read(), version)

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='memo_ms',
      version=version["__version__"],
      description='Python package to perform MS2 Based Sample Vectorization and visualization',
      long_description=readme(),
      long_description_content_type='text/x-rst',
      url='https://github.com/mandelbrot-project/memo',
      author='Arnaud Gaudry',
      author_email='arnaud.gaudry@unige.ch',
      classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
      ],
      packages=find_packages(exclude=['*tests*']),
      python_requires=">=3.7",
      install_requires=[
          'ipykernel',
          'pandas',
          'numpy',
          'jupyter >= 1.0.0',
          'matchms >= 0.9.0',
          'spec2vec >= 0.4',
          'plotly >= 4.14.3',
          'cimcb-lite >= 1.0.2',
          'scikit-bio >= 0.5.6', 
          'scikit-learn >= 0.24.1'
      ],
      extras_require={"dev": ["isort>=4.2.5,<5",
                            "prospector[with_pyroma]",
                            "pytest",
                            "pytest-cov",],
                     },
      zip_safe=False)
