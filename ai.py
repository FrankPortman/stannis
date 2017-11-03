import copy

def score(game, victory):
    if victory:
        if victory == u' ❌':
            return 10
        return -10
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
            new_game.turn += 1
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
            new_game.turn += 1
            val, _ = minimax(new_game, True)
            if val < best_score:
                best_score = val
                best_move = (r_move, c_move)
        return best_score, best_move
