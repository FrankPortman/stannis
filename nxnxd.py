import random

'''
Generalized n x n x d tic tac toe. 
You need d in a row on an n x n grid to win.
'''

# Marks to strings
X = ' X'
O = ' O'

class Board(object):
    '''
    Board and all that fun stuff.
    '''
    def __init__(self, n, d):
        self.n = n
        self.d = d
        self.board = [[None] * n] * n

    def print_board(self):
        print('----' * self.n)
        for row in self.board:
            print(*[i if i == X or i == O else '  ' for i in row], sep=" |")
            print('----' * self.n)

    def _direction_checker(self, row_dir=0, col_dir=0):
        '''
        Returns a function that checks a certain row direction or column
        direction or both (diagonal). We use these to construct the broader
        victory checkers.

        col_dir / row_dir should be either 0 if they don't vary for a 
        specific check, +1 if you want an increasing checker or -1 if you want a
        decreasing checker.

        Returns number of matches equal to board(row, col) in a single direction,
        returning 0 if the first step in said direction is not equal to board(row, col).

        This whole thing is probably uglier than it needs to be, but the 
        optimizations it offers over a full brute force each time make the AI 
        work marginally better. *shrug*
        '''

        def checker(row, col):
            '''
            Try at most (d - 1) in a given direction and stop early if we hit 
            an edge. Only need (d - 1) in any given direction since we are only
            looking for matches on a given (row, col), adding 1 later.
            '''
            val = self.board[row][col]
            matches = 0

            for i in range(1, self.d):
                cr = row + row_dir * i
                cc = col + col_dir * i
                if cr < 0 or cc < 0:
                    break
                if cr >= self.n or cc >= self.n:
                    break
                if self.board[cr][cc] != val:
                    break
                matches += 1
            return matches
        return checker

    def check_victory(self, row, col):
        if self.board[row][col] is None:
            return False

        def make_scorer(row_dirs, col_dirs):
            def scorer():
                score = 1 
                for row_dir, col_dir in zip(row_dirs, col_dirs):
                    checker = self._direction_checker(row_dir=row_dir, 
                                                      col_dir=col_dir)
                    score += checker(row, col)
                    if score >= self.d:
                        return self.board[row][col]
                return False
            return scorer

        horizontal_scorer = make_scorer([0, 0], [-1, 1])
        vertical_scorer = make_scorer([-1, 1], [0, 0])
        diagonal_scorer = make_scorer([-1, 1], [-1, 1])
        antidiag_scorer = make_scorer([-1, 1], [1, -1])

        return horizontal_scorer() or \
               vertical_scorer()   or \
               diagonal_scorer()   or \
               antidiag_scorer()

    def move(self, player, row, col):
        self.board[row][col] = player
        self.turn += 1


class Game(object):
    ''' 
    A single game of nxnxd Tic Tac Toe.
    '''

    def __init__(self, n, d):
        self.board = Board(n, d)
        self.turn = 0
        self.current = X if random.random() < 0.5 else O

    def play_game(game):
        while True:
            self.board.move(self.current, row, col)
            if self.board.check_victory(row, col):
                #self.current wins
                break
        # prompt user
        #