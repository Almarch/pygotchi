from setuptools import setup, Extension
import pybind11
import os

ext_modules = [
    Extension(
        "tamalib",
        sources=["src/tamalib.cpp"],
        include_dirs=[pybind11.get_include()]
    )
]

setup(
    name="pygotchi",
    version="0.0.0",
    ext_modules=ext_modules,
    zip_safe=False,
)