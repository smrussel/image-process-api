import tensorflow as tf
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np

import os

# basedir = os.path.abspath(os.path.dirname(__file__))
# path = basedir + '/models/vgg16_weights_tf_dim_ordering_tf_kernels.h5'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model_three = VGG16(weights='imagenet')

# model_three = VGG16()
# model_three.load_weights(path)



def model_three_func(path):
    img_path = path
    # There is an interpolation method to match the source size with the target size
    # image loaded in PIL (Python Imaging Library)
    img = tf.keras.preprocessing.image.load_img(img_path, color_mode='rgb', target_size=(224, 224))
    # display(img)
    # Converts a PIL Image to 3D Numy Array
    x = tf.keras.preprocessing.image.img_to_array(img)
    # x.shape
    # Adding the fouth dimension, for number of images
    x = np.expand_dims(x, axis=0)

    # mean centering with respect to Image
    x = preprocess_input(x)
    features = model_three.predict(x)
    p = decode_predictions(features)
    return p
