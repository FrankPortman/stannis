import copy
from functools import lru_cache

from nxnxd import Game

def score(game, victory, depth=0):
    if victory:
        if victory == u' ❌':
            return 10 - depth
        return depth - 10
    return 0

def minimax(game, player):
    victory = game.board.get_board_state()
    moves = game.board.get_available_moves()

    if victory or moves == []:
        # print('scoring!')
        return score(game, victory), None

    # `player` is maximizing
    if player:
        best_score = float('-inf')
        for r_move, c_move in moves:
            new_game = copy.deepcopy(game)
            new_game.move(r_move, c_move)
            # print('({}, {}) has score'.format(r_move, c_move))
            val, _ = minimax(new_game, False)
            # print('{}'.format(val))
            if val > best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move

    else:
        best_score = float('inf')
        for r_move, c_move in moves:
            new_game = copy.deepcopy(game)
            new_game.move(r_move, c_move)
            val, _ = minimax(new_game, True)
            if val < best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move


def minimax2(game, player, victory=False):
    moves = game.board.get_available_moves()

    if victory or moves == []:
        return score(game, victory), None

    if player:
        best_score = float('-inf')
        for r_move, c_move in moves:
            new_game = copy.deepcopy(game)
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            # print('({}, {}) has score'.format(r_move, c_move))
            val, _ = minimax2(new_game, False, victory)
            # print('{}'.format(val))
            if val > best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move

    else:
        best_score = float('inf')
        for r_move, c_move in moves:
            new_game = copy.deepcopy(game)
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            val, _ = minimax2(new_game, True, victory)
            if val < best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move


def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

@lru_cache(maxsize=None)
def minimax3(game, player, victory=False):
    moves = game.board.get_available_moves()

    if victory or moves == []:
        return score(game, victory), None

    if player:
        best_score = float('-inf')
        for r_move, c_move in moves:
            new_game = copy.deepcopy(game)
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            # print('({}, {}) has score'.format(r_move, c_move))
            val, _ = minimax3(new_game, False, victory)
            # print('{}'.format(val))
            if val > best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move

    else:
        best_score = float('inf')
        for r_move, c_move in moves:
            new_game = copy.deepcopy(game)
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            val, _ = minimax3(new_game, True, victory)
            if val < best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move

def minimax4(game, player, victory=False):
    moves = game.board.get_available_moves()

    if victory or moves == []:
        return score(game, victory), None

    if player:
        best_score = float('-inf')
        for r_move, c_move in moves:
            new_game = Game(game.board.n, game.board.d, game.players, game.mode, game.turn, [x[:] for x in game.board.board])
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            val, _ = minimax4(new_game, False, victory)
            if val > best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move

    else:
        best_score = float('inf')
        for r_move, c_move in moves:
            new_game = Game(game.board.n, game.board.d, game.players, game.mode, game.turn, [x[:] for x in game.board.board])
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            val, _ = minimax4(new_game, True, victory)
            if val < best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move


def alphabeta(game, player, alpha=float('-inf'), beta=float('inf'), victory=False, depth=0):
    MAX_DEPTH = 5

    moves = game.board.get_available_moves()

    if depth == MAX_DEPTH or victory or moves == []:
        return score(game, victory), None

    depth += 1

    if player:
        best_score = float('-inf')
        for r_move, c_move in moves:
            new_game = Game(game.board.n, game.board.d, game.players, game.mode, game.turn, [x[:] for x in game.board.board])
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            val, _ = alphabeta(new_game, False, alpha, beta, victory, depth)
            if val > best_score:
                best_score = val
                best_move = (r_move, c_move)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return best_score, best_move

    else:
        best_score = float('inf')
        for r_move, c_move in moves:
            new_game = Game(game.board.n, game.board.d, game.players, game.mode, game.turn, [x[:] for x in game.board.board])
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            val, _ = alphabeta(new_game, True, alpha, beta, victory, depth)
            if val < best_score:
                best_score = val
                best_move = (r_move, c_move)
            beta = min(beta, val)
            if beta <= alpha:
                break 
        return best_score, best_move


# def alphabeta(game, player):
#     MAX_DEPTH = 5

#     moves = game.board.get_available_moves()

#     if depth == MAX_DEPTH or victory or moves == []:
#         return score(game, victory), None

#     depth += 1

#     def min_or_max_play(f):
#         best_score = -1 * f(-1, 1) * float('inf')
#         for r_move, c_move in moves:
#             new_game = Game(game.board.n, 
#                             game.board.d, 
#                             game.players, 
#                             game.mode, 
#                             game.turn, 
#                             game.board.copy())
#             new_game.move(r_move, c_move)
#             victory = new_game.board.check_victory(r_move, c_move)
#             val, _ = alphabeta(new_game, not player, alpha, beta, victory, depth)
#             is_new_best = val > best_score if f(-1, 1) == 1 else val < best_score
#             if is_new_best:
#                 best_score = val
#                 best_move = (r_move, c_move)

def negamax(game, player, alpha=float('-inf'), beta=float('inf'), victory=False, depth=0):
    '''
    Negamax + alphabeta pruning
    '''
    MAX_DEPTH = 5

    moves = game.board.get_available_moves()

    if depth == MAX_DEPTH or victory or moves == []:
        return player * score(game, victory), None

    depth += 1

    best_score = float('-inf')
    for r_move, c_move in moves:
        new_game = Game(game.board.n, 
                        game.board.d, 
                        game.players, 
                        game.mode, 
                        game.turn, 
                        game.board.copy())
        new_game.move(r_move, c_move)
        victory = new_game.board.check_victory(r_move, c_move)
        val, _ = negamax(new_game, -player, -beta, -alpha, victory, depth)
        val = -val
        if val > best_score:
            best_score = val
            best_move = (r_move, c_move)
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return best_score, best_move


def negamax2(game, player, alpha=float('-inf'), beta=float('inf'), victory=False, depth=0):
    '''
    Negamax + alphabeta pruning
    '''
    MAX_DEPTH = 5

    moves = game.board.get_available_moves()

    if depth == MAX_DEPTH or victory or moves == []:
        return player * score(game, victory), None

    depth += 1

    best_score = float('-inf')
    for r_move, c_move in moves:
        game.move(r_move, c_move)
        victory = game.board.check_victory(r_move, c_move)
        val, _ = negamax(game, -player, -beta, -alpha, victory, depth)
        val = -val
        game._undo(r_move, c_move)
        if val > best_score:
            best_score = val
            best_move = (r_move, c_move)
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return best_score, best_move


class AI(object):
    def next_move(self):
        pass
    def serialize(self):
        # Convert board + args to hash
        pass

class Backend(object):
    def __init__(self):
        self.cache = Cache()

# tuple([tuple(x[:]) for x in a.board.board[:]])
# function alphabeta(node, depth, α, β, maximizingPlayer)
# 02      if depth = 0 or node is a terminal node
# 03          return the heuristic value of node
# 04      if maximizingPlayer
# 05          v := -∞
# 06          for each child of node
# 07              v := max(v, alphabeta(child, depth – 1, α, β, FALSE))
# 08              α := max(α, v)
# 09              if β ≤ α
# 10                  break (* β cut-off *)
# 11          return v
# 12      else
# 13          v := +∞
# 14          for each child of node
# 15              v := min(v, alphabeta(child, depth – 1, α, β, TRUE))
# 16              β := min(β, v)
# 17              if β ≤ α
# 18                  break (* α cut-off *)
# 19          return v
# version where only the list 

# start = timer(); minimax(a, True) ; end = timer() ; print(end - start)
# start = timer(); minimax2(a, True) ; end = timer() ; print(end - start)
# start = timer(); minimax3(a, True) ; end = timer() ; print(end - start)
# start = timer(); minimax4(a, True) ; end = timer() ; print(end - start)
# start = timer(); minimax5(a, True) ; end = timer() ; print(end - start)