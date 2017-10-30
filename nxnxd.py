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

    def _direction_checker(self, col_dir=0, row_dir=0):
        '''
        Returns a function that checks a certain row direction or column
        direction or both (diagonal). We use these to construct the broader
        victory checkers.

        col_dir / row_dir should be either 0 if they don't vary for a 
        specific check, +1 if you want an increasing checker or -1 if you want a
        decreasing checker.

        We use absolute values of distances to the edge of the board to abstract
        positive/negative cases for increasing vs decreasing traversal.

        Returns number of matches equal to board(row, col) in a single direction,
        returning 0 if the first step in said direction is not equal to board(row, col).

        TODO: do this recursively to patent any d continguous tiles (any direction, even multiple)
        tic tac toe. At each step count (# adjacent cells - 1) until none. Each one returns the max
        adjaceny path it can find.

        This whole thing is probably uglier than it needs to be, but the optimizations it offers
        over a full brute force each time make the AI work marginally better. *shrug*
        '''
        def get_limits(pos, dir):
            '''
            Returns distance to edge, given step direction.
            '''
            if dir == 1:
                return self.n - pos - 1
            if dir == -1:
                return pos

        def checker(row, col):
            val = self.board[row][col]
            score = 0

            if val is None:
                return score

            limits = [self.d]
            # In order not to take the min of NoneTypes
            if row_dir:
                limits.append(get_limits(row, row_dir))
            if col_dir:
                limits.append(get_limits(col, col_dir))

            limit = min(limits)

            for i in range(1, limit + 1):
                if self.board[row + row_dir * i][col + col_dir * i] != val:
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

        horizontal_checker = make_checker(self._direction_checker(col_dir=1, row_dir=0),
                                          self._direction_checker(col_dir=-1, row_dir=0))

        vertical_checker = make_checker(self._direction_checker(col_dir=0, row_dir=1),
                                        self._direction_checker(col_dir=0, row_dir=-1))

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