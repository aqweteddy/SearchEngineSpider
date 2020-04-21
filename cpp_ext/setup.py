from distutils.core import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize("urlPool.pyx"), extra_compile_args=["-O3"] )