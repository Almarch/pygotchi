from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "pygotchi._tamalib",
        sources=["src/tamalib.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
        extra_compile_args=["-std=c++11"]
    )
]

setup(
    name="pygotchi",
    version="0.0.0",
    packages=["pygotchi"],
    ext_modules=ext_modules,
    install_requires=["pybind11"]
)
