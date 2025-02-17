import os
import matplotlib.image as mpimg

_pkg_dir = os.path.dirname(__file__)
background = mpimg.imread(os.path.join(_pkg_dir, "img", "background.png"))

icons = {}

for icon in [
    "attention",
    "bathroom",
    "food",
    "game",
    "lights",
    "medicine",
    "status",
    "training"
]:
    icons[icon] = mpimg.imread(os.path.join(_pkg_dir, "img", icon + ".png"))
