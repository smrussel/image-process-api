import base64
from io import BytesIO
from PIL import Image

import tensorflow as tf

from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
import numpy as np

# import os
# basedir = os.path.abspath(os.path.dirname(__file__))
# path = basedir+'/models/mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224.h5'
# print(basedir)

model_one = MobileNetV2(weights='imagenet')
# model_one = MobileNetV2()
# model_one.load_weights(path)


def model_one_func(img):
    with open(img, "rb") as f:
        im_b64 = base64.b64encode(f.read())

    im_bytes = base64.b64decode(im_b64)  # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    img = Image.open(im_file)
    img = img.resize((224, 224))

    # Preprocessing the image
    x = tf.keras.preprocessing.image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='tf')

    preds = model_one.predict(x)
    pred_proba = "{:.3f}".format(np.amax(preds))  # Max probability
    pred_class = decode_predictions(preds, top=1)  # ImageNet Decode

    result = str(pred_class[0][0][1])  # Convert to string
    result = result.replace('_', ' ').capitalize()
    return (result, pred_proba)