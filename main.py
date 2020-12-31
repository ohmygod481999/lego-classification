from flask import Flask, jsonify, request, render_template
import os
import tensorflow as tf
from utils import getClassNames
import numpy as np

app = Flask(__name__)

class_names = getClassNames()

IMG_PATH = 'upload-img'

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route('/')
def root():
    return jsonify({
        "name": "hihihi"
    })

@app.route('/api/predict', methods=['POST'])
def predictImg():
    files = request.files
    print(files)
    if 'img' not in files:
        return jsonify({
            'success': False
        })
    f = files['img']
    img_path = os.path.join(IMG_PATH, f.filename)
    f.save(img_path)
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(256,256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predictions = model.predict(img_array)
    scores = tf.nn.softmax(predictions[0])
    score_with_label = []
    for i in range(len(scores)):
        score_with_label.append({
            'score': float(scores[i]),
            'label': class_names[i]
        })
    sorted_score_with_label = sorted(score_with_label, key=lambda k: k['score'], reverse=True)
    print(sorted_score_with_label)
    # predict_label = class_names[np.argmax(score)]
    return jsonify({
        'success': True,
        'predicts': sorted_score_with_label
    })

if __name__ == "__main__":
    model = tf.keras.models.load_model(os.path.join('model'))
    
    app.run(debug=True)