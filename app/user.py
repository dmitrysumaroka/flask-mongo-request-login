# -*- coding: utf-8 -*-
# @Author: Dima Sumaroka
# @Date:   2017-01-23 13:06:16
# @Last Modified by:   Dima Sumaroka
# @Last Modified time: 2017-02-06 11:12:55

from werkzeug.security import check_password_hash, generate_password_hash
from passlib.apps import custom_app_context as pwd_context
from app import app
from datetime import datetime
from bson import json_util

class User():

    def __init__(self, id):
        self.username = None
        self.email = None
        self.id = id
        self.password_hash = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_email(self, email):
        self.email = email

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def build_user(user):
        userObj = User(json_util.dumps(user['_id']))
        userObj.username = user['username']
        userObj.email = user['email']
        userObj.password_hash = user['password_hash']
        return userObj


    def set_radius(self, radius):
        self.radius = radius

    def save(self):
        self.id = app.mongo.db.user.insert({
                "username": self.username,
                "password_hash": self.password_hash,
                "email": self.email,
                "createtedAt": datetime.now()
            })
        if self.id:
            return True
        else:
            return False