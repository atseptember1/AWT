"""
- Load all images from directory
- Crop, downscale, upscale each image
- Creat:
    * Sub-image = 32*32*3
    * Sub-label = 20*20*3
    * stride = 14
"""
import os
import glob
import numpy as np
from tools import get_image, crop, resize
from tqdm import tqdm

#Define some constants
lr_size = 32
hr_size = 20
stride = 14
pad = 6

#Get image paths
img_dir = "ukbench100"
img_dir_path = os.path.join(os.getcwd(), img_dir)
img_paths = sorted(glob.glob(os.path.join(img_dir_path,"*.jpg")))

#Create 2 list for storing sub-images and sub-labels
inputs = []
outputs = []


#Load all images from directory
for img_path in tqdm(img_paths):
    #Load image and convert to array
    o_image = get_image(img_path)
    #Crop image
    o_image = crop(o_image, 2)
    #Downscale, upscale image
    d_image = resize(o_image, 1/2)
    d_image = resize(d_image, 2)
    d_image = d_image/255.
    
    rows, cols = o_image.shape[:2]
    #Create sub-image, sub-label
    for r in range(0, rows - lr_size, stride):
        for c in range(0, cols - lr_size, stride):
            sub_image = d_image[r:r+lr_size, c:c+lr_size]
            sub_label = o_image[r+pad:r+pad+hr_size, c+pad:c+pad+hr_size]
            inputs.append(sub_image)
            outputs.append(sub_label)

#Save dataset
inputs = np.array(inputs)
outputs = np.array(outputs)
print(inputs.shape, outputs.shape)

np.save("inputs.npy", inputs)
np.save("outputs.npy", outputs)

