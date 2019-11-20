from datetime import datetime
# from config import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import UserMixin
from dictalchemy import make_class_dictable

# from model import *

db = SQLAlchemy()


class ModelWrapper:
    bcrypt = None
    login_manager = None

    def __init__(self, app):
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
        db.init_app(app)
        self.bcrypt = Bcrypt(app)
        self.login_manager = LoginManager(app)
        self.login_manager.login_view = 'login'
        self.login_manager.login_message_category = 'info'

        # to manage sessions,
        @self.login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))


make_class_dictable(db.Model)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    received = db.Column(db.Integer)
    give_balance = db.Column(db.Integer)
    admin = db.Column(db.Integer)

    # history = db.relationship('History', backref='username', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.give_balance}','{self.received}')"


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    r_time = db.Column(db.DateTime, nullable=False)
    senduser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    getuser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"History('{self.id}','{self.amount}', '{self.r_time}', '{self.senduser_id}','{self.getuser_id}')"

class Redeem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    reuser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    redeemtime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Redeem('{self.reuser_id}', '{self.amount}', '{self.redeemtime}'')"


def _create_database():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    _ = ModelWrapper(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
