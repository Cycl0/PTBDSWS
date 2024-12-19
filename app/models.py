from . import db

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role', lazy='dynamic')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True, index=True)
    user_last_name = db.Column(db.String(64))
    user_ip = db.Column(db.String(64))
    user_host = db.Column(db.String(64))
    user_inst = db.Column(db.String(64))
    user_disc = db.Column(db.String(64))
    user_role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

