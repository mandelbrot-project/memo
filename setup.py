from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='memo',
      version='0.0.1',
      description='Python package to perform MS2 Based Sample Vectorization and visualization',
      long_description=readme(),
      url='https://github.com/mandelbrot-project/memo',
      author='Arnaud Gaudry',
      author_email='arnaud.gaudry@unige.ch',
      license='GNU General Public License v3.0',
      packages=['memo'],
      install_requires=[
          'ipykernel',
          'pandas',
          'jupyter >= 1.0.0',
          'matchms >= 0.9.0',
          'spec2vec >= 0.4',
          'plotly >= 4.14.3',
          'cimcb-lite >= 1.0.2',
          'scikit-learn >= 0.24.1',
          'scikit-bio >= 0.5.6',
      ],
      zip_safe=False)