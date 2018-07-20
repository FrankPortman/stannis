from abc import ABC, abstractmethod


class Player(ABC):
	def __init__(self, name):
		self.name = name

	@abstractmethod
	def get_move(self):

class HumanPlayer(Player):
	

class AIPlayer(Player):
	def __init__(self, AI):
		self.AI = AI

	def make_move(self, board):
		self.AI.