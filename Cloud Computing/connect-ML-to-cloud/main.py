import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"

import tensorflow as tf
from tensorflow import keras
import numpy as np

model = keras.models.load_model("")

from flask import Flask, request, jsonify

def transform_text(text):
    data = np.asarray(text)
    data = data / 255.0
    data = data[np.nrewaxis, ..., np.newaxis]
    data = tf.image.resize(data, [28,28])
    return data

def predict(x):
    predictions = model(x)
    predictions = tf.nn.softmax(predictions)
    pred0 = predictions[0]
    label0 = np.argmax(pred0)
    return label0

app = Flask(__name__)

@app.route("/",methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is not None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            pass
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"