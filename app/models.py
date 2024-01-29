from app import app, db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    status = db.Column(db.String(40), default='admin')
    profile_picture = db.Column(
        db.String(400), default='profile_pictures/default.jpg')

    def __repr__(self) -> str:
        return f'{self.status}:{self.name}'


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # email = db.Column(db.String(50), unique=True, default='notusable@gmail.com',)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', backref='customers')

    def __repr__(self) -> str:
        return f'{self.id}->{self.name}'
