from abc import ABC, abstractmethod


class Player(ABC):
	def __init__(self, name='Bobert'):
		self.name = name

	@abstractmethod
	def get_move(self):
		pass

class HumanPlayer(Player):
	def get_move(self, game_state, verbose):
		if verbose:
			print('Moves available to player: {}'.format(game_state.get_available_moves))
		return input('Choose your move: ')

	
class AIPlayer(Player):
	def __init__(self, AI, name='Computron'):
		super().__init__(name)
		self.AI = AI

	def get_move(self, game_state):
		self.AI.next_best_move(game_state)
