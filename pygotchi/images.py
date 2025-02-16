import os
import matplotlib.image as mpimg

_pkg_dir = os.path.dirname(__file__)
_background_path = os.path.join(_pkg_dir, "data", "background.png")
background = mpimg.imread(_background_path)