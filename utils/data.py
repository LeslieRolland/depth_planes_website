import numpy as np
from numpy import asarray
from PIL import Image
import tempfile

### Loading an image
def load_image(image_file):
    if image_file is not None:
        image = Image.open(image_file)
        return image
    return None

def save_temp_image(image):
    if image is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            image.save(tmp.name)
            return tmp.name
    return None

def img_to_array(image_file):
    if image_file is not None:
        image = Image.open(image_file)
        image_data = asarray(image)
        return image_data
    return None

def array_to_image(image_array):
    image = Image.fromarray(image_array)
    tmp_name = save_temp_image(image)
    return image,tmp_name
