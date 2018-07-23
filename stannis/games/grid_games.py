from itertools import product

from stannis import game, player
from stannis.games.grid_utils import ALL_DIR_SCORERS, GridBoard as Board


class NxDxK(game.Game):
    '''
    NxD grid with K in a row to win. Typically played using Tic Tac Toe pieces.
    '''
    def __init__(self, players, n=3, d=3, k=3, pieces=[' ❌ ', ' ⭕ ']):
        super().__init__(players)
        self.n = n
        self.d = d
        self.k = k
        self.pieces = pieces
        self.Board = Board(n, d)
        # Explore making this just a list comprehension each time
        self.available_moves = set(product(range(n), range(d)))

    @property
    def current_player_piece(self):
        return self.pieces[self._current_player]
    
    def get_available_moves(self, player):
        '''
        Both players have access to all remaining moves.
        '''
        return self.available_moves

    def _get_available_moves(self, player):
        return [
            (r, c) for r, c 
            in product(range(self.n), range(self.d)) 
            if self.board[r][c] is None
        ]

    def _handle_player_move(move):
        return tuple(int(x) for x in move.split(','))

    def make_move(self, player, row, col):
        self.available_moves.remove((row, col))
        self.Board[row][col] = player
        self.turn += 1

    def _undo(self, row, col):
        '''
        Use with care, primarily for AI.
        '''
        self.available_moves.add((row, col))
        self.Board[row][col] = None
        self.turn -= 1

    def check_victory(self, row, col):
        if not self.Board[row][col]:
            return False, None

        for scorer in ALL_DIR_SCORERS:
            print(scorer(self.Board, row, col))
            if scorer(self.Board, row, col) >= self.k:
                return True, self.Board[row][col]

        return False, None

    def play(self, verbose=False):
        print('Player 1: {}'.format(self.players[0].name))
        print('Player 2: {}'.format(self.players[1].name))

        while True:
            print('\n\n')
            print(self.Board)
            print("Player {}, {}'s turn".format(self._current_player, 
                                                 self.current_player.name))

            move = self.current_player.get_move(self, verbose=verbose)
            if isinstance(self.current_player, player.HumanPlayer):
                move = self._handle_player_move(move)

            self.make_move(self.current_player_piece,
                           *move)

            victory, who = self.check_victory(*move)
            if victory:
                print(self.Board)
                print('Winner {}!'.format(who))
                return who

            if self.is_game_over(self.current_player):
                print(self.Board)
                print('Tie.')
                return None 


class ColumnNxDxK(NxDxK):
    '''
    Similar to regular class except you move by playing into columns, e.g. Connect4.
    '''
    def __init__(self, players, n=6, d=7, k=4, pieces=[' 🔴 ', ' 🔵 ']):
        super().__init__(players, n, d, k, pieces)
        self.column_fill = [0 for _ in range(d)]
        self.available_moves = set([col for col in range(d)])

    def _handle_player_move(self, move):
        return [int(move)]

    def col_to_row_col(self, col):
        return self.n - self.column_fill[col] - 1, col

    def make_move(self, player, col):
        row, col = self.col_to_row_col(col)
        self.Board[row][col] = player
        self.column_fill[col] += 1
        self.turn += 1

    def _undo(self, col):
        row, col = self.col_to_row_col(col)
        self.Board[row + 1][col] = None
        self.column_fill[col] -= 1
        self.turn -= 1

    def check_victory(self, col):
        row, col = self.col_to_row_col(col)
        return super().check_victory(row + 1, col)

    def get_available_moves(self, player):
        '''
        Returns coordinates that aren't `None` so the bot can do its thang.
        For connect 4, we only need to check if the first row is empty. Placing
        a move does the check for where a piece actually ends up.
        '''
        return [
            col for col, val 
            in enumerate(self.column_fill)
            if val < self.n
        ]


def TicTacToe(players):
    return NxDxK(players)


def Connect4(players):
    return ColumnNxDxK(players)


if __name__ == '__main__':
    from stannis.player import HumanPlayer
    TicTacToe([HumanPlayer('Billy'), HumanPlayer('Bob')]).play()
