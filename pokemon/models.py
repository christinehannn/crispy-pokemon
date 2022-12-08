from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

from pokemon import (
    db,
    login_manager,
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(
        db.String(120),
        nullable=False,
        default='default.jpg'
    )
    password = db.Column(db.String(60), nullable=False)
    pokemons = db.relationship('Pokemon', backref='trainer', lazy=True)

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, expires_sec)['user_id']
            return User.query.get(user_id)
        except:
            pass

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Pokemon(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_caught = db.Column(
        db.DateTime,
        nullable=True,
    )
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    def __repr__(self):
        return f"Pokemon('{self.title}', '{self.date_posted}')"
