from flask import Flask, jsonify, request, render_template, send_from_directory
import os
import tensorflow as tf
from utils import getClassNames
import numpy as np

app = Flask(__name__)

IMG_PATH = 'upload-img'
DATA_PATH = 'croped_lego'


@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route(f'/{IMG_PATH}/<path:path>')
def imagesUpload(path):
    return send_from_directory(IMG_PATH, path)

@app.route(f'/{DATA_PATH}/<path:path>')
def imagesData(path):
    return send_from_directory(DATA_PATH, path)


@app.route('/api/labels')
def getLabels():
    labels = [label for label in os.listdir(os.path.join(
        '.', DATA_PATH)) if os.path.isdir(os.path.join(DATA_PATH, label))]
    return jsonify({
        'labels': labels
    })


@app.route('/api/legos')
def getLegos():
    labels = [label for label in os.listdir(os.path.join(
        '.', DATA_PATH)) if os.path.isdir(os.path.join(DATA_PATH, label))]
    data = dict()
    for label in labels:
        data[label] = [img for img in os.listdir(os.path.join(
            DATA_PATH, label)) if os.path.isfile(os.path.join(DATA_PATH, label, img))]
    return jsonify(data)

@app.route('/api/unlabel-legos')
def getUnlabelLegos():
    files = [f for f in os.listdir(os.path.join(
        '.', IMG_PATH)) if os.path.isfile(os.path.join(IMG_PATH, f))]
    return jsonify(files)


@app.route('/api/predict', methods=['POST'])
def predictImg():
    files = request.files
    if 'img' not in files:
        return jsonify({
            'success': False
        })
    f = files['img']
    img_path = os.path.join(IMG_PATH, f.filename)
    f.save(img_path)
    img = tf.keras.preprocessing.image.load_img(
        img_path, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    predictions = model.predict(img_array)
    scores = tf.nn.softmax(predictions[0])
    score_with_label = []
    # get classnames
    labels = [label for label in os.listdir(os.path.join(
        '.', DATA_PATH)) if os.path.isdir(os.path.join(DATA_PATH, label))]
    for i in range(len(scores)):
        score_with_label.append({
            'score': float(scores[i]),
            'label': labels[i]
        })
    sorted_score_with_label = sorted(
        score_with_label, key=lambda k: k['score'], reverse=True)
    return jsonify({
        'success': True,
        'predicts': sorted_score_with_label
    })


if __name__ == "__main__":
    model = tf.keras.models.load_model(os.path.join('model'))

    app.run(debug=True)
