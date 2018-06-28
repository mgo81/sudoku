#!flask/bin/python
from flask import request
from flask import jsonify
from flask import abort

import hiscore.hiscore_model as model

def get_hiscores():
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    if not category:
        category = "all"
    cat_string = ""
    cat_value = ""
    if category != "all" and category != "own":
        abort(400)
    else: 
        if category == "own":
            token = request.headers.get('X-Authorization')
            print(token)
            if not token:
                abort(401)
            user = model.get_user(token)
            if len(user) == 0:
                abort(401)
            user = user[0]["user_id"]
            cat_string = " WHERE users.user_id = %s "
            cat_value = [user]
    if difficulty:
        difficulty_id = model.get_difficulty(difficulty)
        if len(difficulty_id) != 1:
            abort(400)
        difficulty_id = difficulty_id[0]["difficulty_id"]
        if len(cat_string) == 0:
            cat_string = " WHERE hiscores.hiscore_difficulty = %s "
            cat_value = [difficulty_id]
        else:
            cat_string += "AND hiscores.hiscore_difficulty = %s "
            cat_value.append(difficulty_id)
    hiscores = model.get_hiscores(cat_string, cat_value)
    return jsonify({'data': hiscores})

def post_hiscores():
    token = request.headers.get('X-Authorization')
    if not token:
        abort(401)
    user = model.get_user(token)
    if len(user) == 0:
        abort(403)
    user = user[0]["user_id"]
    try:
        score = int(request.json["score"])
        difficulty = request.json["difficulty"]
    except:
        abort(400)
    if score < 0 or not difficulty:
        abort(400)
    difficulty_id = model.get_difficulty(difficulty)
    if len(difficulty_id) != 1:
        abort(400)
    difficulty_id = difficulty_id[0]["difficulty_id"]
    inserted = model.insert_hiscore(user, score, difficulty_id)
    return jsonify({'data': inserted})
