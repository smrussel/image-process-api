import tensorflow as tf
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
import numpy as np
from keras.applications.resnet import ResNet50

import os
# basedir = os.path.abspath(os.path.dirname(__file__))
# path = basedir + '/models/resnet50_weights_tf_dim_ordering_tf_kernels.h5'

model_two = ResNet50(weights='imagenet')

# model_two = ResNet50()
# model_two.load_weights(path)


def model_two_func(path):
    original = tf.keras.preprocessing.image.load_img(path, target_size=(224, 224))
    numpy_image = tf.keras.preprocessing.image.img_to_array(original)
    image_batch = np.expand_dims(numpy_image, axis=0)
    processed_image = preprocess_input(image_batch, mode='caffe')
    preds = model_two.predict(processed_image)
    pred_class = decode_predictions(preds, top=1)
    return pred_class