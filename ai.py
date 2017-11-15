import nxnxd as g

def score(game, victory, depth=0):
    if victory:
        if victory == u' ❌':
            return 10 - depth
        return depth - 10
    return 0


def minimax4(game, player, victory=False):
    moves = game.board.get_available_moves()

    if victory or moves == []:
        return score(game, victory), None

    if player:
        best_score = float('-inf')
        for r_move, c_move in moves:
            new_game = g.Game(game.board.n, game.board.d, game.players, game.mode, game.turn, [x[:] for x in game.board.board])
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
            new_game = g.Game(game.board.n, game.board.d, game.players, game.mode, game.turn, [x[:] for x in game.board.board])
            new_game.move(r_move, c_move)
            victory = new_game.board.check_victory(r_move, c_move)
            val, _ = minimax4(new_game, True, victory)
            if val < best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move


def alphabeta(game, player, alpha=float('-inf'), beta=float('inf'), victory=False, depth=0):
    MAX_DEPTH = 6

    moves = game.board.get_available_moves()

    if depth == MAX_DEPTH or victory or moves == []:
        return score(game, victory), None

    depth += 1

    if player:
        best_score = float('-inf')
        for r_move, c_move in moves:
            new_game = g.Game(game.board.n, game.board.d, game.players, game.mode, game.turn, [x[:] for x in game.board.board])
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
            new_game = g.Game(game.board.n, game.board.d, game.players, game.mode, game.turn, [x[:] for x in game.board.board])
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


def negamax2(game, player, alpha=float('-inf'), beta=float('inf'), victory=False, depth=0):
    '''
    Negamax + alphabeta pruning
    '''
    MAX_DEPTH = 7

    moves = game.board.get_available_moves()

    if depth == MAX_DEPTH or victory or moves == []:
        return player * score(game, victory, depth), None

    best_score = float('-inf')
    for r_move, c_move in moves:
        game.move(r_move, c_move)
        victory = game.board.check_victory(r_move, c_move)
        val, _ = negamax2(game, -player, -beta, -alpha, victory, depth + 1)
        val = -val
        game._undo(r_move, c_move)
        if val > best_score:
            best_score = val
            best_move = (r_move, c_move)
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return best_score, best_move


from collections import namedtuple

LOWERBOUND, EXACT, UPPERBOUND = -1,0,1

class TranspositionTable(object):
    '''
    Stateful transposition tables (memoization).
    '''
    Entry = namedtuple('Entry', ['flag', 'value'])

    def __init__(self):
        cache = {}

    def __getitem__(self, key):
        return cache.get(key, None)

    def __setitem__(self, key, flag, value):
        cache[key] = Entry(flag, value)


class Negamax(object):

    def __init__(self, max_depth=7, tt=TranspositionTable()):
        self.max_depth = max_depth
        self.tt = tt

    def lookup(self, node):
        self.tt[node] 

class AI(object):
    def next_move(self):
        pass
    def serialize(self):
        # Convert board + args to hash
        pass

class Backend(object):
    def __init__(self):
        self.cache = Cache()

# start = timer(); minimax(a, True) ; end = timer() ; print(end - start)
# start = timer(); minimax2(a, True) ; end = timer() ; print(end - start)
# start = timer(); minimax3(a, True) ; end = timer() ; print(end - start)
# start = timer(); minimax4(a, True) ; end = timer() ; print(end - start)
# start = timer(); minimax5(a, True) ; end = timer() ; print(end - start)