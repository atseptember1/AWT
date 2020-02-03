import numpy as np 

from tqdm import tqdm 
from tensorflow.keras import models
from tools import get_image, crop, resize
from PIL import Image
from keras_preprocessing.image import img_to_array, array_to_img

image_path="960x540.png"
image = Image.open(image_path)
height, width = get_image(image_path).shape[:2]
#print(get_image("960x540.png").shape)
#print(height, width)

size = (int(width*2)+12, int(height*2)+12)
resize_image = image.resize(size, Image.BICUBIC)
#resize_image.save("resize.png", "PNG")
resize_image = img_to_array(resize_image)
resize_image = resize_image/255.
rows, cols = resize_image.shape[:2]

lr_size = 32
hr_size = 20
stride = 14
pad = 6

print(resize_image.shape)

model = models.load_model("best_model_checkpoint.h5")

output = []
for r in tqdm(range(0, height*2 - hr_size + 1, hr_size)):
    for c in range(0, width*2 - hr_size + 1, hr_size):
        sub_image = resize_image[r:r+lr_size, c:c+lr_size]
        output.append(sub_image)

output = model.predict(np.array(output))

test = np.zeros([height*2, width*2, 3])
i = 0
for r in tqdm(range(0, height*2 - hr_size + 1, hr_size)):
    for c in range(0, width*2 - hr_size + 1, hr_size):
        test[r:r+hr_size, c:c+hr_size] = output[i]
        i += 1

test = array_to_img(test)
test.save("test_05.png", "PNG")

""" output = np.zeros([height*2, width*2, 3])
for r in tqdm(range(0, height*2 - hr_size + 1, hr_size)):
    for c in range(0, width*2 - hr_size + 1, hr_size):
        sub_image = resize_image[r:r+lr_size, c:c+lr_size]
        sub_image = np.expand_dims(sub_image, axis=0)
        assert sub_image.shape == (1,32,32,3), "not correct input dimension"
        pred_image = model.predict(sub_image)
        pred_image = pred_image.reshape((hr_size, hr_size, 3))
        output[r:r+hr_size, c:c+hr_size] = pred_image

output = array_to_img(output)
output.save("test_03.png", "PNG") """

