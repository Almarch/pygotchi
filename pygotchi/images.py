import os
import matplotlib.image as mpimg

_pkg_dir = os.path.dirname(__file__)
background = mpimg.imread(os.path.join(_pkg_dir, "www", "img", "p1", "background.png"))

icons = {}

for icon in ["icon" + str(x) for x in range(8)]:
    icons[icon] = mpimg.imread(os.path.join(_pkg_dir, "www", "img", "p1", icon + ".png"))
