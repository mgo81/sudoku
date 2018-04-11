from random import *

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
    cell = range(1,10)[:]
    shuffle(cell)
    for row in range(9):
        for column in range(9):
            available[row][column] = cell[:]
    return available[:]

def print_grid(puzzle):
    """prints puzzle as a grid"""
    for row in puzzle:
        print(row)

def main():
    """main"""
    puzzle = create_puzzle()
    available = create_available()
    print_grid(puzzle)
    print_grid(available)

main()