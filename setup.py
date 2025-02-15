from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "tama_module",
        sources=["src/Tamagotchi.cpp"],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=["-std=c++11"],
    )
]

setup(
    name="tama_module",
    version="0.1.0",
    ext_modules=ext_modules,
    zip_safe=False,
)