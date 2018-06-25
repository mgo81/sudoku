#!flask/bin/python
from flask import Flask
from flask import abort
from flask import request
from flask import jsonify

from random import *

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
    shuffle(cell)
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
            x = randint(0,difficulty)
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
    puzzle = generate_puzzle()
    if difficulty == "easy":
        puzzle = empty_squares(puzzle, 3)
    elif difficulty == "medium":
        puzzle = empty_squares(puzzle, 2)
    elif difficulty == "hard":
        puzzle = empty_squares(puzzle, 1)
    else:
        abort(400)
    return jsonify({'puzzle': puzzle})

@app.route('/api/v1/puzzle/check', methods=['GET'])
def check_puzzle():
    return

@app.route('/api/v1/puzzle/solution', methods=['GET'])
def get_solution():
    return

"""
user
"""
@app.route('/api/v1/user/signup', methods=['POST'])
def signup():
    return

@app.route('/api/v1/user/login', methods=['POST'])
def login():
    return

@app.route('/api/v1/user/logout', methods=['POST'])
def logout():
    return

"""
hiscores
"""
@app.route('/api/v1/hiscores', methods=['GET'])
def get_hiscores():
    return 

@app.route('/api/v1/hiscores', methods=['POST'])
def post_hiscores():
    return 



if __name__ == '__main__':
    app.run(debug=True)