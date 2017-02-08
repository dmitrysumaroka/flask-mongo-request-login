# -*- coding: utf-8 -*-
# @Author: Dima Sumaroka
# @Date:   2017-01-23 13:08:19
# @Last Modified by:   Dima Sumaroka
# @Last Modified time: 2017-02-08 14:15:54

from app import app, lm
from flask import request, session
from flask_login import login_user, logout_user, login_required
from .user import User
from bson import json_util, ObjectId
import json
import base64

@app.route('/login', methods=['POST'])
def login():
    response = {
        "success": False,
        "response": " "
    }
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password:
        user = app.mongo.db.user.find_one({"username": username})
        if user and User.validate_login(user["password_hash"], password):
            user_obj = User.build_user(user)
            if login_user(user_obj):
                userSession = {
                    'userId': user['_id'],
                    'session_id': session["_id"],
                    'success': True
                }
                app.mongo.db.session.insert(userSession)
                app.mongo.db.session.update({
                    "userId" : ObjectId(user['_id'])
                },
                {
                    "$set": {
                        "session_id": session['_id']
                    }
                }, upsert=True)
                return json_util.dumps(userSession)
        else:
            response["response"] = "Worng password"
            return json.dumps(response)
    else:
        response["response"] = "Username or password not entered"
        return json.dumps(response)

@app.route('/logout')
def logout():
    response = {
        "success": False,
        "response": " "
    }
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        userFromSession = app.mongo.db.session.find_one({"session_id": api_key})
        if userFromSession:
            deleteUser = app.mongo.db.session.remove({'_id': userFromSession['_id']}, True)
            if deleteUser:
                response['success'] = True
                response['response'] = "User Logged out"
            else:
                response['response'] = "Something went wrong"
        else:
            response['success'] = True
            response['response'] = "User Logged out"
        logout_user()
    return json.dumps(response)

@app.route('/write', methods=['GET'])
@login_required
def write():
    return json.dumps({"success": True})

@lm.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        userFromSession = app.mongo.db.session.find_one(
            {
                "session_id": api_key
            })
        if userFromSession:
            user = app.mongo.db.user.find_one(
                {
                    "_id": ObjectId(userFromSession['userId'])
                })

            user_obj = User.build_user(user)
            if user_obj:
                return user_obj
            else:
                return None
        else:
            return None

@app.route('/register', methods=['POST'])
def new_user():
    response = {
        "success": False,
        "response": " "
    }
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if username is None or password is None:
        response["response"] = "username or pass not provided"
        return json.dumps(response)

    if app.mongo.db.user.find_one({"username": username}) is not None:
        response["response"] = "username taken"
        return json.dumps(response)

    user = User("")
    user.username = username
    user.hash_password(password = password)
    user.set_email(email = email)

    if user.save():
        response["success"] = True
        response["response"] = "User saved"
        response["userId"] = user.id
        response = json.dumps(response, default=json_util.default)
    return json.dumps(response)
