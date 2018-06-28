#!flask/bin/python
from flask import request
from flask import jsonify
from flask import abort

import puzzle.puzzle_model as model

def get_puzzle():
    try:
        difficulty = request.args.get('difficulty')
    except:
        abort(400)
    if not difficulty or difficulty not in ["easy", "medium", "hard"]:
        abort(400)
    difficulty_id = model.get_difficulty(difficulty)
    puzzle = model.generate_puzzle()
    puzzle = model.empty_squares(puzzle, difficulty_id)
    return jsonify({'data': puzzle})

def check_puzzle():
    solution = False
    try:
        puzzle = request.json["puzzle"]
        if model.check_solution(puzzle):
            solution = True
    except:
        abort(400)
    return jsonify({'data': solution})

def get_solution():
    try:
        puzzle = request.json["puzzle"]
        puzzle = model.generate_solution(puzzle)
    except:
        abort(400)
    return jsonify({'data': puzzle})