from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='time_domain_trispectrum_cython',
    ext_modules=cythonize('tdts_cython.pyx'),
    zip_safe=False,
    include_dirs=[numpy.get_include()]
)
