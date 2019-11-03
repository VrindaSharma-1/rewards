from datetime import datetime
from flaskblog import db,login_manager
from flask_login import UserMixin

# to manage sessions,
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    received = db.Column(db.Integer)
    give_balance = db.Column(db.Integer)
    # history = db.relationship('History', backref='username', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.give_balance}','{self.received}')"

# class History(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     r_hist=db.Column(db.Integer)
#     r_time = db.Column(db.DateTime, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.give_balance}','{self.received}')"
