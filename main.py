from flask import Flask, jsonify, request, render_template
import os
import tensorflow as tf
from utils import getClassNames
import numpy as np
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class_names = getClassNames()

IMG_PATH = 'upload-img'

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route('/list_user')
def list_user():
    users = db.session.query(User).all()
    return jsonify({
        'user': users[0].username
    })

@app.route('/add_user')
def add_user():
    user = User(id=2, username="hello", email="vuongbaolong48@gmail.com")
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return "some thing wrong"
    return "ok"

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
    return jsonify({
        'success': True,
        'predicts': sorted_score_with_label
    })

if __name__ == "__main__":
    model = tf.keras.models.load_model(os.path.join('model'))
    
    app.run(debug=True)