#!flask/bin/python
from flask import Flask
from flask import abort
from flask import request
from flask import jsonify
import pymysql.cursors
import bcrypt

import random

import string

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='Sudoku',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def query(sql, values=""):
    try:
        with connection.cursor() as cursor:
            if values != "":
                cursor.execute(sql, values)
                result = cursor.fetchall()
            else:
                cursor.execute(sql)
                result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close
    return result

def check_solution(puzzle):
    """checks if sudoku puzzle is correct"""
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return False
            num = puzzle[i][j]
            puzzle[i][j] = 0
            if check_cell(puzzle, i, j, num):
                puzzle[i][j] = num
            else:
                return False
    return True

def create_puzzle():
    """creates a 9x9 grid of 0"""
    column = [0] * 9
    puzzle = []
    for i in range(9):
        puzzle.append(column[:])
    return puzzle[:]

def create_available():
    """list of available possible numbers for each cell"""
    available = create_puzzle()
    cell = []
    for i in range(1,  10):
        cell.append(i)
    random.shuffle(cell)
    for row in range(9):
        for column in range(9):
            available[row][column] = cell[:]
    return available[:]

def create_adjustable(puzzle):
    """determines which cells are adjustable"""
    adjustable = create_puzzle()
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                adjustable[i][j] = 1
    return adjustable[:]


def print_grid(puzzle):
    """prints puzzle as a grid"""
    for row in puzzle:
        print(row)

def check_cell(puzzle, i, j, num):
    """checks if number can be placed in that cell"""
    for k in range(9):
        if num == puzzle[k][j] or num == puzzle[i][k]:
            return False
    i = i//3 * 3
    j = j//3 * 3
    upper_i = i + 3
    upper_j = j + 3
    while i < upper_i:
        while j < upper_j:
            if num == puzzle[i][j]:
                return False
            j += 1
        j -= 3    
        i += 1
    return True

def generate_solution(puzzle):
    """generates a correct solution or prints a statement 
    depending if the puzzle can be solved"""
    available = create_available()
    adjustable = create_adjustable(puzzle)
    i, j = 0, 0
    count = 0
    previous = 1
    while i < 9:
        j = 0
        while j < 9:
            if i < 0:
                print("no solution")
                return []
            count += 1
            if count > 100000:
                print(count)
                print("cant be solved")
                return []
            if adjustable[i][j]:
                puzzle[i][j] = 0
                try:
                    while True:
                        num = available[i][j][0]
                        available[i][j] = available[i][j][1:]
                        if (check_cell(puzzle, i, j, num)):
                            puzzle[i][j] = num
                            break
                    j += 1
                    previous = 1
                except IndexError:
                    available[i][j] = range(1,10)[:]
                    puzzle[i][j] = 0
                    if j > 0:
                        j -= 1
                        previous = -1
                    else:
                        i -= 1
                        j = 8
    
            else:
                if previous == 1:
                    j += 1
                else:
                    if j > 0:
                        j -= 1
                    else:
                        i -= 1
                        j = 8
        i += 1
    return puzzle

def generate_puzzle():
    """Generates a random correct sudoku board"""
    puzzle = create_puzzle()
    available = create_available()
    i, j, = 0, 0
    while i < 9:
        j = 0
        while j < 9:
            try:
                while True:
                    num = available[i][j][0]
                    available[i][j] = available[i][j][1:]
                    if (check_cell(puzzle, i, j, num)):
                        puzzle[i][j] = num
                        break
                j += 1
            except IndexError:
                available[i][j] = range(1,10)[:]
                puzzle[i][j] = 0
                if j > 0:
                    j -= 1
                else:
                    i -= 1
                    j = 8
                puzzle[i][j] = 0
        i += 1
    return puzzle

def empty_squares(puzzle, difficulty):
    """makes some squares empty depending on difficulty level"""
    for i in range(9):
        for j in range(9):
            x = random.randint(0,difficulty)
            if x == 0:
                puzzle[i][j] = 0
    return puzzle

app = Flask(__name__)



"""
puzzle
"""
@app.route('/api/v1/puzzle/generate', methods=['GET'])
def get_puzzle():
    difficulty = request.args.get('difficulty')
    if not difficulty or difficulty not in ["easy", "medium", "hard"]:
        abort(400)
    data = query("SELECT difficulty_id FROM difficulties WHERE difficulty_name = %s", (difficulty))
    puzzle = generate_puzzle()
    puzzle = empty_squares(puzzle, data[0]["difficulty_id"])
    return jsonify({'puzzle': puzzle})

@app.route('/api/v1/puzzle/check', methods=['POST'])
def check_puzzle():
    puzzle = request.json["puzzle"]
    solution = False
    if check_solution(puzzle):
        solution = True
    return jsonify({'solution': solution})

@app.route('/api/v1/puzzle/solution', methods=['POST'])
def get_solution():
    puzzle = request.json["puzzle"]
    puzzle = generate_solution(puzzle)
    return jsonify({'puzzle': puzzle})
        

"""
user
"""
@app.route('/api/v1/user/signup', methods=['POST'])
def signup():
    username = request.json["username"]
    password = request.json["password"].encode()
    if not username or not password:
        abort(400)
    salt = "yeet"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    data = query("SELECT user_name FROM Users")
    for user in data:
        if user["user_name"] == username:
            abort(400)
    data = query("INSERT INTO Users (user_name, user_hash, user_token) VALUES (%s, %s, %s);", (username, hashed, token))
    return jsonify({'data': data})

@app.route('/api/v1/user/login', methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json["password"].encode()
    if not username or not password:
        abort(400)
    data = query("SELECT user_hash FROM Users WHERE user_name = %s", (username))
    hash = data[0]["user_hash"].encode()
    if bcrypt.checkpw(password, hash):
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
        data = query("UPDATE Users SET user_token = %s WHERE user_name = %s", (token, username))
    else:
        abort(400)
    return jsonify({'data': data})

@app.route('/api/v1/user/logout', methods=['POST'])
def logout():
    username = request.json["username"]
    password = request.json["password"].encode()
    if not username or not password:
        abort(400)
    data = query("SELECT user_hash FROM Users WHERE user_name = %s", (username))
    hash = data[0]["user_hash"].encode()
    if bcrypt.checkpw(password, hash):
        data = query("UPDATE Users SET user_token = %s WHERE user_name = %s", (None, username))
    else:
        abort(400)
    return jsonify({'data': data})

"""
hiscores
"""
@app.route('/api/v1/hiscores', methods=['GET'])
def get_hiscores():
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    if not category:
        category = "all"
    token = request.headers.get('X-Authorization')
    data = query("SELECT user_id FROM users WHERE user_token = %s",(token))
    cat_string = ""
    cat_value = ""
    if category != "all" and category != "own":
        print("yeet")
        abort(400)
    else: 
        if category == "own" and len(data) == 1:
            cat_string = " WHERE users.user_id = %s "
            cat_value = [data[0]["user_id"]]
    if difficulty:    
        data = query("SELECT difficulty_id FROM difficulties WHERE difficulty_name = %s", (difficulty))
        if len(data) == 1:
            if len(cat_string) == 0:
                cat_string = " WHERE hiscores.hiscore_difficulty = %s "
                cat_value = [data[0]["difficulty_id"]]
            else:
                cat_string += "AND hiscores.hiscore_difficulty = %s "
                cat_value.append(data[0]["difficulty_id"])
    
    data = query("""SELECT hiscores.hiscore_time, users.user_name, difficulties.difficulty_name 
        FROM hiscores 
        INNER JOIN users ON users.user_id = hiscores.hiscore_user_id
        INNER JOIN difficulties ON difficulties.difficulty_id = hiscores.hiscore_difficulty
        """ + cat_string + """
        ORDER BY hiscores.hiscore_time
        LIMIT 10""", tuple(cat_value))
        
    return jsonify({'data': data})

@app.route('/api/v1/hiscores', methods=['POST'])
def post_hiscores():
    token = request.headers.get('X-Authorization')
    if not token:
        abort(401)
    data = query("SELECT user_id FROM users WHERE user_token = %s", (token))
    if len(data) == 0:
        abort(403)
    user = data[0]["user_id"]
    try:
        score = int(request.json["score"])
    except ValueError:
        abort(400)
    difficulty = request.json["difficulty"]
    if score < 0 or difficulty not in ["easy", "medium", "hard"]:
        abort(400)
    data = query("SELECT difficulty_id FROM difficulties WHERE difficulty_name = %s", (difficulty))
    data = query("INSERT INTO Hiscores (hiscore_user_id, hiscore_time, hiscore_difficulty) VALUES (%s, %s, %s)", (user, score, data[0]["difficulty_id"]))

    return jsonify({'data': data})



if __name__ == '__main__':
    app.run(debug=True)