from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Lego(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(120), unique=True, nullable=False)
    label = db.Column(db.Integer, db.ForeignKey('label.id'), nullable=True)
    status = db.Column(db.String(30), nullable=False)
