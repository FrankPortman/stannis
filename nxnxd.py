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

    # def check_victory(self, row, col):
    #     '''
    #     This should short circuit on both the high level directional
    #     checks as well as inside each directional checker.
    #     '''
    #     val = self.board[row][col]

    #     # horizontal score
    #     score = 1
    #     # to the right
    #     for i in range(min(row - self.n, self.d)):
    #         if self.board[row][col + i + 1] != val:
    #             break
    #         score += 1
    #     # to the left
    #     for i in range(min(self.n - row, self.d)):
    #         if self.board[row][col - i - 1] != val:
    #             break
    #         score += 1

    #     if score >= self.d:
    #         return val

    #     # vertical score
    #     score = 1
    #     # down
    #     for i in range(min(col - self.n, self.d)):
    #         if self.board[row + i + 1][col] != val:
    #             break
    #         score += 1
    #     # up
    #     for i in range(min(self.n - col, self.d)):
    #         if self.board[row - i - 1][col] != val:
    #             break
    #         score += 1

    #     if score >= self.d:
    #         return val

    #     # main diagonal
    #     score = 1
    #     # down
    #     for i in range(min(col - self.n, row - self.n, self.d)):
    #         if self.board[row + i + 1][col + i + 1] != val:
    #             break
    #         score += 1
    #     # up
    #     for i in range(min(self.n - col, self.n - row, self.d)):
    #         if self.board[row - i - 1][col - i - 1] != val:
    #             break
    #         score += 1

    #     if score >= self.d:
    #         return val

    #     # anti diagonal
    #     score = 1
    #     # down
    #     for i in range(min(col - self.n, self.n - row, self.d)):
    #         if self.board[row + i + 1][col - i - 1] != val:
    #             break
    #         score += 1

    #     # up
    #     for i in range(min(self.n - col, row = self.n, self.d)):
    #         if self.board[row - i - 1][col + i + 1] != val:
    #             break
    #         score += 1

    #     if score >= self.d:
    #         return val

    #     return False

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
        def horizontal_checker(row, col):
            return 1 + \
                   self._direction_checker(col_dir=1, row_dir=None)(row, col) + \
                   self._direction_checker(col_dir=-1, row_dir=None)(row, col)
        def vertical_checker(row, col):
            return 1 + \
                   self._direction_checker(col_dir=None, row_dir=1)(row, col) + \
                   self._direction_checker(col_dir=None, row_dir=-1)(row, col)
        def diagonal_checker(row, col):
            return 1 + \
                   self._direction_checker(col_dir=1, row_dir=1)(row, col) + \
                   self._direction_checker(col_dir=-1, row_dir=-1)(row, col)
        def antidiag_checker(row, col):
            return 1 + \
                   self._direction_checker(col_dir=1, row_dir=-1)(row, col) + \
                   self._direction_checker(col_dir=-1, row_dir=1)(row, col)

        return horizontal_checker(row, col) == self.d or \
               vertical_checker(row, col) == self.d   or \
               diagonal_checker(row, col) == self.d   or \
               antidiag_checker(row, col) == self.d

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