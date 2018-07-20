from __future__ import print_function

from abc import ABC, abstractmethod

X = u' ❌ '
O = u' ⭕ '

class BaseBoard(ABC):
    '''
    Generic abstract base class for a Board defined as an n x d grid
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

    def copy_board(self):
        return [row[:] for row in self.board]

    def to_immutable(self):
        return tuple([tuple(row) for row in self.board])

    def serialize(self):
        return str(self.board)

    @abstractmethod
    def get_available_moves(self):
        pass

    @abstractmethod
    def move(self):
        pass


# 3 -> 16
# 4 -> 23
# 5 -> 29
# 6 -> 35

# 3 -> 12 + 2
# 4 -> 16 + 3
# 5 -> 29
# 6 -> 35