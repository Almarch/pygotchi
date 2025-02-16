from .Tama import Tama

import importlib.resources
import matplotlib.image as mpimg
from PIL import Image
import io

background = importlib.resources.open_binary("data", "background.jpg")
background = io.BytesIO(background.read())
background = Image.open(background)
background = mpimg.pil_to_array(background)
