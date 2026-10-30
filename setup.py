from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "pygotchi._tamalib",
        sources=[
            "src/tamalib.cpp",
            "src/tamalib/cpu.c",
            "src/tamalib/hw.c",
            "src/tamalib/tamalib.c",
        ],
        include_dirs=[pybind11.get_include(), "src/tamalib"],
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
        "pygotchi.www.img",
        "pygotchi.www.img.p1",
        "pygotchi.www.img.p2",
        "pygotchi.www.img.angel",
    ],
    ext_modules=ext_modules,
    install_requires=["pybind11"],
    package_data={
        "pygotchi": [
            "www/**/*", 
            "www/img/**/*",
            "www/img/p1/*.png",
            "www/img/p2/*.png",
            "www/img/angel/*.png",
        ],
    },
    include_package_data=True,
)
