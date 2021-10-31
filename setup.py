from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='memo_ms',
      version='0.0.4',
      description='Python package to perform MS2 Based Sample Vectorization and visualization',
      long_description=readme(),
      url='https://github.com/mandelbrot-project/memo',
      author='Arnaud Gaudry',
      author_email='arnaud.gaudry@unige.ch',
      classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
      ],
      packages=['memo_ms'],
      install_requires=[
          'ipykernel',
          'pandas',
          'numpy',
          'jupyter >= 1.0.0',
          'matchms >= 0.9.0',
          'spec2vec >= 0.4',
          'plotly >= 4.14.3',
          'cimcb-lite >= 1.0.2',
          'scikit-learn >= 0.24.1',
          'scikit-bio >= 0.5.6'
      ],
      extras_require={"dev": ["isort>=4.2.5,<5",
                            "prospector[with_pyroma]",
                            "pytest",
                            "pytest-cov",],
                     }
      python_requires=">=3.8",
      zip_safe=False)
