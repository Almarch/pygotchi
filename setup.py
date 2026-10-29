from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "pygotchi._tamalib",
        sources=[
            "src/tamalib.cpp",
            "tamalib/cpu.c",
            "tamalib/hw.c",
            "tamalib/tamalib.c",
        ],
        include_dirs=[pybind11.get_include(), "tamalib"],
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
        "pygotchi.www.img.background",
        "pygotchi.www.img.background.p1",
        "pygotchi.www.img.background.p2",
        "pygotchi.www.img.background.angel",
        "pygotchi.www.img.icons",
        "pygotchi.www.img.icons.p1",
        "pygotchi.www.img.icons.p2j",
        "pygotchi.www.img.icons.angel",
    ],
    ext_modules=ext_modules,
    install_requires=["pybind11"],
    package_data={
        "pygotchi": [
            "www/**/*", 
            "www/img/**/*",
            "www/img/background/p1/*.png",
            "www/img/background/p2/*.png",
            "www/img/background/angel/*.png",
            "www/img/icons/p1/*.png",
            "www/img/icons/p2j/*.png",
            "www/img/icons/angel/*.png",
        ],
    },
    include_package_data=True,
)
