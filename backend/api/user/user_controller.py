#!flask/bin/python
from flask import request
from flask import jsonify
from flask import abort
import bcrypt
import string
import random

import user.user_model as model

def authentication():
    try:
        username = request.json["username"]
        password = request.json["password"].encode()
    except:
        abort(400)
    if not username or not password:
        abort(400)
    try:
        hashed = model.get_hash(username).encode()
    except:
        abort(401)
    if bcrypt.checkpw(password, hashed):
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    else:
        abort(401)
    return token  

def signup():
    try:
        username = request.json["username"]
        password = request.json["password"].encode()
    except:
        abort(400)
    if not username or not password:
        abort(400)
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    user_name = model.get_username()
    for user in user_name:
        if user["user_name"] == username:
            abort(400)
    inserted = model.insert_user(username, hashed, token)
    return jsonify({'data': inserted})

def login():
    try:
        username = request.json["username"]
    except:
        abort(400)
    token = authentication()
    added = model.add_token(token, username)

    return jsonify({'data': added})

def logout():
    token = request.headers.get('X-Authorization')
    if not token:
        abort(401)
    user = model.get_user_t(token)
    if len(user) == 0:
        abort(403)
    user = user[0]["user_id"]
    removed = model.remove_token(user)
    return jsonify({'data': removed})


