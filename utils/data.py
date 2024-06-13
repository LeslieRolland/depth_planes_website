import numpy as np
from numpy import asarray
from PIL import Image
import tempfile
import zipfile
import os

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
    # print(image)
    # print(tmp_name)
    return image,tmp_name

def save_mask_image(image_array):
    dict_mask_image = {}

    for k, v in enumerate(image_array):
        if v.dtype != np.uint8:
            v = (255 * (v - np.min(v)) / (np.max(v) - np.min(v))).astype(np.uint8)
        image, path = array_to_image(v)
        dict_mask_image[f"plan{k}"] = path

    return dict_mask_image

def create_zip_file(file_dict):
    zip_path = "mask_images.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for name, file_path in file_dict.items():
            zipf.write(file_path, os.path.basename(file_path))
    return zip_path
