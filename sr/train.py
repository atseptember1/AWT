import numpy as np
from tools import SRCNN
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

inputs = np.load("inputs.npy")
outputs = np.load("outputs.npy")

num_epoch = 100
batch_size = 800
height, width, channel = inputs.shape[1:]

model = SRCNN.build(height, width, channel)
optimizer = optimizers.Adam(lr=0.001, decay=0.001/num_epoch)
model.compile(optimizer = optimizer, loss="mse")

early_stopping = EarlyStopping(monitor="loss", patience=5)
checkpoint = ModelCheckpoint(filepath="best_model_checkpoint.h5", monitor="loss", save_best_only=True)

history = model.fit(inputs, outputs, epochs=num_epoch, batch_size=batch_size, callbacks=[early_stopping, checkpoint])