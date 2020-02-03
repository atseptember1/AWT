from tensorflow.keras import models, layers

class SRCNN:
    def build(height, width, channel):
        model = models.Sequential()
        model.add(layers.Conv2D(64, (9,9), activation="relu", kernel_initializer='he_normal', input_shape=(height, width, channel)))
        model.add(layers.Conv2D(32, (1,1), activation="relu", kernel_initializer='he_normal'))
        model.add(layers.Conv2D(channel, (5,5), activation="relu", kernel_initializer='he_normal'))
        
        return model
