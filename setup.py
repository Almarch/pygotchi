from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "pygotchi._tamalib",
        sources=["src/tamalib.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++"
    )
]

setup(
    name="pygotchi",
    version="0.0.0",
    python_requires=">=3.10",
    packages=[
        "pygotchi",
        "pygotchi.www",
        "pygotchi.www.img"
    ],
    ext_modules=ext_modules,
    install_requires=["pybind11"],
    package_data={
        "pygotchi": [
            "www/**/*"
        ],
    },
    include_package_data=True,
)
