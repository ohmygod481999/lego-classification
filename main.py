from flask import Flask, jsonify, request, render_template, send_from_directory
import os
import tensorflow as tf
from utils import getClassNames
import numpy as np
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Lego(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(120), unique=True, nullable=False)
    label = db.Column(db.Integer, db.ForeignKey('label.id'), nullable=True)
    status = db.Column(db.String(30), nullable=True)

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)


labels = db.session.query(Label).all()
label_array = list(map(lambda x: x.name, labels))

IMG_PATH = 'upload-img'

@app.route('/predict')
def predict():
    return render_template("predict.html")
    
@app.route(f'/{IMG_PATH}/<path:path>')
def images(path):
    return send_from_directory(IMG_PATH, path)

@app.route('/api/labels')
def getLabels():
    labels = db.session.query(Label).all()
    lbs = []
    for lb in labels:
        lbs.append({
            'id': lb.id,
            'name': lb.name
        })
    return jsonify({
        'labels': lbs
    })

@app.route('/api/legos')
def getLegos():
    legos = db.session.query(Lego).all()
    lgs = []
    for lg in legos:
        lgs.append({
            'id': lg.id,
            'path': lg.path,
            'status': lg.status
        })
    return jsonify({
        'legos': lgs
    })

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
    lego = Lego(path=IMG_PATH + '/' + f.filename, status="unlabel")
    db.session.add(lego)
    db.session.commit()
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(256,256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predictions = model.predict(img_array)
    scores = tf.nn.softmax(predictions[0])
    score_with_label = []
    # get classnames
    print(label_array)
    for i in range(len(scores)):
        score_with_label.append({
            'score': float(scores[i]),
            'label': label_array[i]
        })
    lego = Lego()
    sorted_score_with_label = sorted(score_with_label, key=lambda k: k['score'], reverse=True)
    return jsonify({
        'success': True,
        'predicts': sorted_score_with_label
    })

if __name__ == "__main__":
    model = tf.keras.models.load_model(os.path.join('model'))
    
    app.run(debug=True)