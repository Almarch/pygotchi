from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "tama_module",
        sources=["src/Tamagotchi.cpp", "src/tamalib.cpp"],
        include_dirs=[pybind11.get_include(), "src"]
    )
]

setup(
    name="pygotchi",
    version="0.0.0",
    ext_modules=ext_modules,
    zip_safe=False,
)