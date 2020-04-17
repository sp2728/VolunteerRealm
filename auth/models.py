import enum
from flask_login import UserMixin
from app import db


class Permission(enum.Enum):
    ADMIN = 1
    USER = 2
    NONE = 10 # can be used to disable users


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(15), unique=True)
    gender = db.Column(db.String(10))
    permission = db.Column(db.Enum(Permission), default=Permission.USER)

