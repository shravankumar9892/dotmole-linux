from flask_login import UserMixin
from app import db, login
from datetime import datetime, timedelta
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

# Database design: https://ondras.zarovi.cz/sql/demo/

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Configurations backref
    configurations = db.relationship('Configuration', backref='user', lazy='dynamic')

    # Livestreams backref
    livestream = db.relationship('Livestream', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    type = db.Column(db.String(10))
    services = db.Column(db.String(200))
    livestream_connected = db.Column(db.Integer)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Livestreams backref
    livestream = db.relationship('Livestream', backref='config', lazy='dynamic')

    def __repr__(self):
        return '<Configuration {}>'.format(self.name)

class Livestream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    internal_ip = db.Column(db.String(100))
    configuration_name = db.Column(db.String(20))
    configuration_type = db.Column(db.String(20))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_configuration = db.Column(db.Integer, db.ForeignKey('configuration.id'))

    def __repr__(self):
        return '<Livestream {}>'.format(self.internal_ip)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))