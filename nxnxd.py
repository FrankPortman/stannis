import random

def compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))

def compose(*fs):
    return reduce(compose2, fs)

'''
Generalized n x n x d tic tac toe. 
You need d in a row on an n x n grid to win.
'''

# Marks to strings
X = ' X'
O = ' O'

class Game(object):
    ''' 
    A single game of nxnxd Tic Tac Toe.
    '''

    def __init__(self, n, d):
        self.n = n
        self.d = d
        self.board = [[None] * n] * n
        self.turn = 0
        self.current = X if random.random() < 0.5 else O

    def print_board(self):
        print('----' * self.n)
        for row in self.board:
            print(*[i if i == X or i == O else '  ' for i in row], sep=" |")
            print('----' * self.n)

    def _direction_checker(self, col_dir=None, row_dir=None):
        '''
        Returns a function that checks a certain row direction or column
        direction or both (diagonal). We use these to construct the broader
        victory checkers.

        col_dir / row_dir should be either `None` if they don't vary for a 
        specific check, +1 if you want an increasing checker or -1 if you want a
        decreasing checker.

        We use absolute values of distances to the edge of the board to abstract
        positive/negative cases for increasing vs decreasing traversal.
        '''
        def make_iterator(dir=None):
            def iterator(i):
                if dir is None:
                    return i
                if dir == 1:
                    return i + 1
                if dir == -1:
                    return -i - 1
            return iterator

        def checker(row, col):
            val = self.board[row][col]
            score = 0

            if val is None:
                return score

            limits = [self.d]
            if col_dir is not None:
                limits.append(self.n - col)
            if row_dir is not None:
                limits.append(self.n - row)

            row_iterator = make_iterator(row_dir)
            col_iterator = make_iterator(col_dir) 
            distances = [abs(x) for x in limits]

            for i in range(min(distances)):
                if self.board[row_iterator(i)][col_iterator(i)] != val:
                    break
                score += 1
            return score

        return checker

    def check_victory(self, row, col):
        def make_checker(*args):
            def checker(row, col):
                score = 1 
                for checker in list(args):
                    score += checker(row, col)
                    if score >= self.d:
                        return self.board[row][col]
                return False
            return checker

        horizontal_checker = make_checker(self._direction_checker(col_dir=1, row_dir=None),
                                          self._direction_checker(col_dir=-1, row_dir=None))

        vertical_checker = make_checker(self._direction_checker(col_dir=None, row_dir=1),
                                        self._direction_checker(col_dir=None, row_dir=-1))

        diagonal_checker = make_checker(self._direction_checker(col_dir=1, row_dir=1),
                                        self._direction_checker(col_dir=-1, row_dir=-1))

        antidiag_checker = make_checker(self._direction_checker(col_dir=1, row_dir=-1),
                                        self._direction_checker(col_dir=-1, row_dir=1))

        return horizontal_checker(row, col) or \
               vertical_checker(row, col)   or \
               diagonal_checker(row, col)   or \
               antidiag_checker(row, col)

    def move(self, player, row, col):
        self.board[row][col] = player
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

        self.move(self.current)
        # prompt user
        #