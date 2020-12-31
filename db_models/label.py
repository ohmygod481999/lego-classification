from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)