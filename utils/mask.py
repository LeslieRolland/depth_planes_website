import numpy as np
import cv2
from utils.data import *

def create_mask_in_one(y_pred, nb_mask: int =None) -> np.array:
    """
    Function to create an array representing categorical mask

    Input:
    y_pred.shape -> (128,256,1)
    """

    slice_ = (np.max(y_pred)+1)/nb_mask
    img_dim = y_pred #reduce the dim
    mask = np.full((nb_mask,img_dim.shape[0],img_dim.shape[1]),-1)

    for i in np.arange(1, nb_mask+1):
        mask[i-1] = np.where((img_dim>=(i-1)*slice_) & (img_dim<i*slice_), i, 0)

    mask = mask.sum(axis=0)

    return mask

def create_mask_from_image(x_array, y_mask_array):

    # x_array = img_to_array(load_image(x_array))
    x_reshape = np.reshape(x_array, (x_array.shape[0]*x_array.shape[1], 3))

    #y_array = cv2.imread(y_path,  cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    #y_reshape = np.reshape(y_array, (y_array.shape[0]*y_array.shape[1]))

    #y_mask_image = np.load(y_mask_array)
    #y_mask_array = cv2.resize(y_mask_image, dsize=(y_array.shape[1], y_array.shape[0]), interpolation=cv2.INTER_NEAREST)
    y_mask_reshape = np.reshape(y_mask_array, (y_mask_array.shape[0]*y_mask_array.shape[1], 1))


    mask_array = np.array([])

    nb_mask = len(np.unique(y_mask_reshape))

    for i in range(nb_mask):
        mask = (y_mask_reshape == i).astype(int)
        mask_x = x_reshape * mask
        mask_array = np.append(mask_array, mask_x)

    mask_array = np.reshape(mask_array, (int(mask_array.shape[0]/3), 3))

    mask_array = mask_array/255

    mask_a = np.expand_dims((mask_array.sum(axis=1) > 0).astype('float64'), axis=-1)
    mask_b = np.concatenate([mask_array,mask_a], axis=1)

    rgba_array = np.reshape(np.asarray(mask_b), (nb_mask, y_mask_array.shape[0], y_mask_array.shape[1], 4))

    return rgba_array

def create_mask_from_image2(x_array :str, y_path: str, y_mask_array):

    # x_array = img_to_array(load_image(x_array))
    x_reshape = np.reshape(x_array, (x_array.shape[0]*x_array.shape[1], 3))

    y_array = cv2.imread(y_path,  cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    y_reshape = np.reshape(y_array, (y_array.shape[0]*y_array.shape[1]))

    y_mask_image = np.load(y_mask_array)
    y_mask_array = cv2.resize(y_mask_image, dsize=(y_array.shape[1], y_array.shape[0]), interpolation=cv2.INTER_NEAREST)
    y_mask_reshape = np.reshape(y_mask_array, (y_mask_array.shape[0]*y_mask_array.shape[1], 1))


    mask_array = np.array([])

    for i in np.unique(y_mask_reshape):
        mask = (y_mask_reshape == i).astype(int)
        mask_x = x_reshape * mask
        mask_array = np.append(mask_array, mask_x)

    mask_array = np.reshape(mask_array, (int(mask_array.shape[0]/3), 3))

    mask_array = mask_array/255

    mask_a = np.expand_dims((mask_array.sum(axis=1) > 0).astype('float64'), axis=-1)
    mask_b = np.concatenate([mask_array,mask_a], axis=1)

    rgba_array = np.reshape(np.asarray(mask_b), (len(np.unique(y_mask_image)), y_array.shape[0], y_array.shape[1], 4))

    return rgba_array
