from __future__ import print_function

import random

board = [[None] * 3 for i in range(3)]
board = [[''] * 3 for i in range(3)]

scores = {
    0: [8, 1, 6],
    1: [3, 5, 7],
    2: [4, 9, 2],
}

scores = {
    0: [2, 7, 6], 
    1: [9, 5, 1], 
    2: [4, 3, 8],
}

def print_board(board):
    for row in board:
        print row

player_1 = 0
player_2 = 0


for row in board:
    print(*row)

for _ in xrange(3):
    print(*(3 * ['*']))

board = [['  '] * 3 for i in range(3)]

def print_board(board):
    print('------------')
    for row in board:
        print(*row, sep=" |")
        print('------------')

board[1][1] = ' X'
board[1][0] = ' O'

print_board(board)

'''
Generalized n x n x d tic tac toe. 
You need d in a row on an n x n grid to win.
'''

class Game(object):
    ''' 
    A single game of nxn Tic Tac Toe.
    Score is stored in a vector of length 2n + 2 where n
    corresponds to the size of the grid you are playing on (n^2 total positions).

    The first n entries correspond to the scores of the rows 1:n respectively.
    The second n entries correspond to the scores of the columns 1:n respectively.
    The second to last entry is the score of the main/leading diagonal.
    The last entry is the score of the antidiagonal.

    'X' wins when they reach score of n in any position.
    'O' wins when they reach score of -n in any position.
    '''
    # backend_chooser = {
    #     'magic': MagicSquare,
    #     'standard': StandardVector,
    # }
    X = ' X'
    O = ' O'

    def __init__(self, n, backend='magic'):
        self.n = n
        # self.backend = self.backend_chooser[backend]
        # self.scorer = self.backend(n)
        self.scores = [[[None] * i] for i in [self.n, self.n, 2]]
        self.scores = [0 for i in range(2 * n + 2)]
        # self.board = [[None] * n for i in range(n)]
        self.pretty_board = [['  '] * n for i in range(n)]
        self.board = self.pretty_board
        self.turn = 0
        self.current = self.X if random.random() < 0.5 else self.O

    def print_board(self):
        print('----' * self.n)
        for row in self.board:
            print(*row, sep=" |")
            print('----' * self.n)

    def update_score(self, who, row, col):
        ''' 
        Updates score for row, column, and diagonals
        based on an X or O being placed.
        '''
        points = {
            self.X: 1,
            self.O: -1,
        }

        point = points[who]
        self.score[0][row] += point
        self.score[1][col] += point
        if row == col: # main diagonal
            self.score[2][0] += point
        if row + col == (self.n - 1): # anti diagonal, off by one inevitable
            self.score[2][1] += point

    def move(self, player, row, col):
        self.board[row][col] = 5
        self.turn += 1

    def _victory_checker(self, which):
        return any([s == which * self.n for s in self.scores])

    @property
    def victory(self):
        if _victory_checker(1):
            return X
        if _victory_checker(-1):
            return O
        return False

    def play_game(game):
        while not game.victory:
            pass
        # prompt user
        #