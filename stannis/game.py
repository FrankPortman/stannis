from abc import ABC, abstractmethod, abstractproperty

class Game(ABC):
	def __init__(self, players):
		''' 
		Could be one player.
		'''
		self.players = players
		self.turn = 0

	@property
	def _current_player(self):
		return self.turn % len(self.players)

	@property
	def current_player(self):
		return self.players[self._current_player]
	

	def is_game_over(self, player):
		return (not self.get_available_moves(player))

	@abstractmethod
	def get_available_moves(self, player):
		pass

	@abstractmethod
	def make_move(self, player):
		'''
		Should usually increment turn.
		'''
		pass

	@abstractmethod
	def _undo(self):
		'''
		Should usually decrement turn.
		Useful for quickly undoing moves in grid search.
		Overwrite if you don't care.
		'''
		pass

	@abstractmethod
	def play(self):
		pass


class TwoPlayerGame(Game):
	'''
	Special class for Two Player Games.
	'''

	def __init__(self):
		pass