#Upscale, Downscale function
#Crop image
import numpy as np
from PIL import Image
from keras_preprocessing.image import load_img, img_to_array, array_to_img

def get_image(path):
    image = load_img(path)
    image_array = img_to_array(image)
    return image_array/255.

def crop(img_array, scale):
    h, w = img_array.shape[:2]
    w -= w % scale
    h -= h % scale
    img_array = img_array[:h, :w, :]
    return img_array

def resize(img_array, scale):
    image = array_to_img(img_array)
    h, w = img_array.shape[:2]
    if scale >= 1 and w % scale != 0 or h % scale !=0:
        raise("Width and Height must be divisors of scale")
    size = (int(w*scale), int(h*scale))
    resize_image = image.resize(size, Image.BICUBIC)
    return img_to_array(resize_image)

