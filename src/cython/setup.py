import os
import re
import sys
from distutils.core import setup
from pyx_replace import pyx_extensions
from Cython.Build import cythonize

setup(
    name='0x88 board',
    ext_modules=cythonize(pyx_extensions(["chess0x88.py"])),
)


def purge(path, pattern):
    for f in os.listdir(path):
        filename = re.search(pattern, f)
        if filename is None:
            pass
        else:
            os.remove(os.path.join(path, f))

if sys.argv[1] == 'clean':
    purge('.', r".*\.c$")
