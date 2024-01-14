# import os
# from datetime import datetime
# import sqlalchemy as sa
# импортируется библиотека SQLAlchemy под псевдонимом sa
from users_policy import UsersPolicy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
# from flask import url_for, current_app
from app import db
# импортируется объект db из модуля app

class Product(db.Model):
    __tablename__ = "products"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False)

class Supply(db.Model):
    __tablename__ = "supplies"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), default=None)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100))

    product = db.relationship('Product', backref=db.backref('supplies', cascade='all, delete-orphan', single_parent=True))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# -----
    # def __init__(self, username, role):
    #     # self.id = id
    #     self.username = username
    #     self.role = role

# Метод, отвечающий за проверку прав
# Метод `can` создает экземпляр класса `UsersPolicy` с переданной записью и подгружает
#  метод `action` этого класса, который отвечает за проверку полномочий пользователя на
#  выполнение данного действия. Если метод найден, то он вызывается и возвращается его
#  результат. Если метод не найден, то возвращается `False`.
    def can(self, action, record = None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False
# -----

    def __repr__(self):
        return '<User %r>' % self.username