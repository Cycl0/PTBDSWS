from . import db

class Disc(db.Model):
    __tablename__ = 'disc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    sem = db.Column(db.String(64))