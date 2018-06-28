#!flask/bin/python
from flask import Flask
import pymysql.cursors
import bcrypt
import random
import string

from config.db import query
import puzzle.puzzle_controller as puzzle
import user.user_controller as user
import hiscore.hiscore_controller as hiscore
app = Flask(__name__)

"""
puzzle
"""
@app.route('/api/v1/puzzle/generate', methods=['GET'])
def get_puzzle():
    return puzzle.get_puzzle()

@app.route('/api/v1/puzzle/check', methods=['POST'])
def check_puzzle():
    return puzzle.check_puzzle()

@app.route('/api/v1/puzzle/solution', methods=['POST'])
def get_solution():
    return puzzle.get_solution()
        

"""
user
"""
@app.route('/api/v1/user/signup', methods=['POST'])
def signup():
    return user.signup()

@app.route('/api/v1/user/login', methods=['POST'])
def login():
    return user.login()

@app.route('/api/v1/user/logout', methods=['POST'])
def logout():
    return user.logout()

"""
hiscores
"""
@app.route('/api/v1/hiscores', methods=['GET'])
def get_hiscores():
    return hiscore.get_hiscores()

@app.route('/api/v1/hiscores', methods=['POST'])
def post_hiscores():
    return hiscore.post_hiscores()

if __name__ == '__main__':
    app.run(debug=True)