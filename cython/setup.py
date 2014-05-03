from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='0x88 board',
    ext_modules=cythonize("*.pyx"),
)
