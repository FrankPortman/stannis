from __future__ import print_function


X = u' ❌ '
O = u' ⭕ '


class GridBoard(object):
    '''
    Generic base class for a GridBoard defined as an n x d grid
    of values or future moves. Common games that might use this are
    Tic-Tac-Toe, Connect-4, Chess, etc.
    '''
    def __init__(self, n, d):
        self.n = n
        self.d = d
        self.board = [[None for _ in range(d)] for _ in range(n)]

    def __repr__(self):
        '''
        Earnest attempt at pretty printing your board to the terminal.
        You may want to override for specific use cases.
        '''
        print('')
        border = '----' * self.d + '-' * (self.d - 1)
        print(border)
        for row in self.board:
            print(*[i or '    ' for i in row], sep="|")
            print(border)
        return ''

    def __str__(self):
        return repr(self)

    def __getitem__(self, idx):
        return self.board[idx]

    def copy_board(self):
        return [row[:] for row in self.board]

    def to_immutable(self):
        return tuple([tuple(row) for row in self.board])

    def serialize(self):
        return str(self.board)


def direction_checker(row_dir=0, col_dir=0):
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

    def checker(Board, row, col):
        '''
        Try at most (d - 1) in a given direction and stop early if we hit 
        an edge. Only need (d - 1) in any given direction since we are only
        looking for matches on a given (row, col), adding 1 later.
        '''
        matches = 0

        # Todo, this should only check up to the victory condition 'k'
        for i in range(1, max(Board.d, Board.n)):
            cr = row + row_dir * i
            cc = col + col_dir * i
            if cr < 0 or cc < 0:
                break
            if cr >= Board.n or cc >= Board.d:
                break
            if Board[cr][cc] != Board[row][col]:
                break
            matches += 1
        return matches
    return checker


def make_scorer(row_dirs, col_dirs):
    def scorer(Board, row, col):
        score = 1
        for row_dir, col_dir in zip(row_dirs, col_dirs):
            checker = direction_checker(row_dir=row_dir,
                                        col_dir=col_dir)
            score += checker(Board, row, col)
        return score
    return scorer


horizontal_scorer = make_scorer([0, 0], [-1, 1])
vertical_scorer = make_scorer([-1, 1], [0, 0])
diagonal_scorer = make_scorer([-1, 1], [-1, 1])
antidiagonal_scorer = make_scorer([-1, 1], [1, -1])


ALL_DIR_SCORERS = [
    horizontal_scorer,
    vertical_scorer,
    diagonal_scorer,
    antidiagonal_scorer,
]
