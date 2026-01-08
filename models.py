from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

db = SQLAlchemy()

class Kanji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kanji = db.Column(db.String(10), nullable=False)
    stroke_order = db.Column(db.String(120), default = 'default.png')
    level = db.Column(db.String(10), nullable=False)
    meanings = db.Column(db.Text, nullable=False)
    kun = db.Column(db.String(200), nullable=False)
    on = db.Column(db.String(200), nullable=False)
    radical = db.Column(db.String(200), nullable=False)
    # vocab = db.Column(db.Integer,nullable=True)
    
class Vocab(db.Model):
    __bind_key__ = "vocab"
    id = db.Column(db.Integer, primary_key=True)
    kanji_list = db.Column(db.String(100),nullable=False)
    vocab = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)