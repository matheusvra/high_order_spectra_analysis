from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='time_domain_trispectrum',
    ext_modules=cythonize('high_order_spectra_analysis/time_domain_trispectrum/tdts_cython.pyx'),
    zip_safe=False,
    include_dirs=[numpy.get_include()]
)
