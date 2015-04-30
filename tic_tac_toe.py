#!/usr/bin/python
import random
from sets import Set

class Game():
	""" a Game between a computer and a human
		This program should beat the human player, although winning is not guaranteed.
	"""
	# all the rows which make a you winner
	tic_tac_toe = [(1, 2, 3), (1, 4, 7), (1, 5, 9), (2, 5, 8), (3, 6, 9), (3, 5, 7), (4, 5, 6), (7, 8, 9)]
	corners = [1, 3, 7, 9]
	edges = [2, 4, 6, 8]
	center = 5
	
	def __init__(self):
		self.human_moves = []
		self.computer_moves = []
		self.messages = ''
		self.computer_turn = True
		self.started_by_computer = True
		self.game_ended = False
		
	def state(self, update = True):
		if update:
			if self.messages == '':
				if self.computer_turn == False and len(self.computer_moves) + len(self.human_moves) != 9:
					self.computer_turn = True
					self.play()
					self.computer_turn = False
				else:
					self.computer_turn = False

			self.end()

		return { 'computer_moves' : self.computer_moves, 'human_moves': self.human_moves, 'messages': self.messages, 'state':self.game_ended }

	def start(self):
		# flip the coin: tail, the computer starts the game
		# head, the human starts the game
		# flip_coin = random.randrange(2)
		# if flip_coin == 0:
		# 	# computer always starts the game from the corners
		# 	cell = random.choice(self.corners)
		# 	return self.update(cell)
		# else:
		# self.messages = "You go first!"
		self.computer_turn = False
		self.started_by_computer = False
		return self.state(False)
			
	def end(self):
		# check for the conditions which ends the game
		for item in self.tic_tac_toe:
			lose = [i for i in item if i in self.human_moves]
			if len(lose) == 3:
				self.messages = 'You win!'
				self.game_ended = True
				return

		for item in self.tic_tac_toe:
			win = [i for i in item if i in self.computer_moves]
			if len(win) == 3:
				self.messages = 'You lost!'
				self.game_ended = True
				return

		# no more empty cells
		if len(self.computer_moves) + len(self.human_moves) == 9:
			self.messages = 'The game ended, it was a tie!'
			self.game_ended = True
			return

	def update(self, cell):
		# update the board with new cell
		if self.game_ended == False:
			print "should get here to update the cell"
			self.messages = ''
			if cell > 9 or cell < 1 or cell is None:
				self.messages = "Incorrect cell! This cell doesn't exist!"

			if cell not in self.human_moves and cell not in self.computer_moves:
				if self.computer_turn:
					self.computer_moves.append(cell)
				else:
					self.human_moves.append(cell)
			else:
				self.messages = "This cell has already been chosen! Please select another one."

		return self.state()

	def play(self):
		# first we check if there is any win situation for the computer
		# if not, we check if there is any win situation for the opponent 
		# and we have to block it
		if self.computer_turn:
			# win or block
			cell = self.win_or_block()

			#  if there's not win or block situation, we check for a
			# fork (double wins)
			if cell is None:
				# check or block a fork
				cell = self.next_move()
				# at this point it does not matter what cell we pick, we are
				# about to tie
				if cell is None:
					empty_cells = list(set([x for x in range(1,10)]) - set(self.computer_moves).union(set(self.human_moves)))
					cell = random.choice(empty_cells)

			self.update(cell)

	def win_or_block(self):
		index = None
		# check for any win position
		for item in self.tic_tac_toe:
			index = None
			indices = [i for i in item if i in self.computer_moves]
			if len(indices) == 2:
				index = list(set(item) - set(indices))
				if index[0] not in self.human_moves:
					# self.game_ended = True
					return index[0]
					break

		# check for any block position		
		for item in self.tic_tac_toe:
			index = None
			indices = [i for i in item if i in self.human_moves]
			if len(indices) == 2:
				index = list(set(item) - set(indices))
				if index[0] not in self.computer_moves:
					return index[0]
					break

		return index
	
	def next_move(self):
		cell = None
		# if the game is started by computer
		if self.started_by_computer:
			if len(self.computer_moves) == 1:
				started_cell = self.computer_moves[0]
				opponent_cell = self.human_moves[0]
				index_corner = self.corners.index(started_cell)
				
				# corners are either on the first column or last column
				if started_cell is not None and opponent_cell is not None:
					# if the opponent choose the center cell, winning is
					# not guaranteed. most likely it'll be a tie
					if opponent_cell == self.center:
						cell = self.corners[len(self.corners) - 1 - index_corner]
					else:
						# the opponent picked any cell other than the center one
						# we could win the game by choosing another corner and
						# creating a fork
						column = started_cell % 3
						if column == 1:
							neighbor_corner_1 = self.corners[index_corner + 1]
							neighbor_corner_2 = self.corners[index_corner + 2 if index_corner + 2 < len(self.corners) else 0]
							
						elif column == 0:
							neighbor_corner_1 = self.corners[index_corner - 1]
							neighbor_corner_2 = self.corners[index_corner - 2 if index_corner - 2 > 0 else len(self.corners) - 1]
							
						if neighbor_corner_1 == opponent_cell or neighbor_corner_2 == opponent_cell:
							cell = neighbor_corner_1 if neighbor_corner_1 != opponent_cell else neighbor_corner_2
						else:
							cell = neighbor_corner_1 if not(neighbor_corner_1 < opponent_cell < started_cell) else random.choice([neighbor_corner_1, neighbor_corner_2])
							
			elif len(self.computer_moves) == 2:
				# try to choose another corner to create a fork situation
				left_corners = list(set(self.corners) - set(self.computer_moves))
				if len(left_corners) > 0:
					if left_corners[0] in self.human_moves:
						cell = left_corners[1]
					elif left_corners[1] in self.human_moves:
						cell = left_corners[0]
					else:
						columns = [x % 3 for x in self.human_moves]
						for item in left_corners:
							if item % 3 not in columns:
								cell = item
								break
						if cell is None:
							cell = random.choice(left_corners)

		# the game is started by a human player
		else:
			# player's got three options to pick to start the game: corners,
			# center and edges

			if len(self.human_moves) == 1:
				opponent_cell = self.human_moves[0]

				# the player chose a corner or an edge as first move
				if opponent_cell in self.corners or opponent_cell in self.edges:
					# the computer should go to the middle. if we're not going
					# to the center, the player can create a fork
					cell = self.center

				# the player chose the center cell as first move
				else:
					# in this situation, player can beat the computer by creating
					# a fork. The best computer could do is a tie depends on
					# how the player plays. Although by picking either corner or edge
					# player can beat the program, we pick corner as selected
					# cell (might be harder for the player to create a fork)
					cell = random.choice(self.corners)

			elif len(self.human_moves) == 2:
				# figure out the second move
				if self.human_moves[0] in self.corners:
					# we pick any edge to block potential fork
					cell = random.choice(list(set(self.edges) - set(self.human_moves)))
				elif self.human_moves[0] in self.edges:
					# pick the corner between edges
					# corners are on the first column or the third
					# we'll find the columns for theses edges first
					columns = [x % 3 for x in self.human_moves if (x % 3 != 2)]
					if len(columns) == 0:
						# both edges are on column two, so any corner is fine
						cell = random.choice(self.corners)
					else:
						# we found the corners which is the same as edge column
						potential_corners = [x for x in self.corners if x % 3 == columns[0]]
						if len(potential_corners) == 1:
							cell = potential_corners[0]
						else:
							if 2 in self.human_moves:
								cell = min(potential_corners)
							else:
								cell = max(potential_corners)
		return cell

if __name__ == "__main__":
	ttt = Game()
	ttt.start()
