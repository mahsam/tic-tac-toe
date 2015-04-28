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
	
	def __init__(self):
		self.human_moves = Set()
		self.computer_moves = Set()
		self.messages = ''
		self.computer_turn = True
		self.game_ended = False
		
	def state(self, update = True):
		if update == True:
			if self.messages == '':
				if self.computer_turn == False:
					self.computer_turn = True
					self.play()
					self.computer_turn = False
				else:
					self.computer_turn = False

			self.end()

		return { 'computer_moves' : list(self.computer_moves), 'human_moves': list(self.human_moves), 'messages': self.messages, 'state':self.game_ended }

	def start(self):
		# computer always starts the game from the corners
		cell = random.choice(self.corners)
		return self.update(cell)
		
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

		game_over = len(self.computer_moves) + len(self.human_moves)
		if game_over == 9:
			self.messages = 'The game ended, it was a tie!'
			self.game_ended = True
			return

	def update(self, cell):
		# update the board with new cell
		if self.game_ended == False:
			self.messages = ''
			if cell > 9 or cell < 1 or cell is None:
				self.messages = "Incorrect cell! This cell doesn't exist!"

			if cell not in self.human_moves and cell not in self.computer_moves:
				if self.computer_turn == True:
					self.computer_moves.add(cell)
				else:
					self.human_moves.add(cell)
			else:
				self.messages = "This cell has already been chosen! Please select another one."

		return self.state()

	def play(self):
		# first we check if there is any win situation for the computer
		# if not, we check if there is any win situation for the opponent 
		# and we have to block it
		if self.computer_turn == True:
			# win or block
			cell = self.win_or_block()

			#  if there's not win or block situation, we check for a fork (double wins)
			if cell is None:
				# check or block a fork
				cell = self.next_move()
				# at this point it does not matter what cell we pick, we are about to tie
				if cell is None:
					empty_cells = list(set([x for x in range(1,10)]) - set(self.computer_moves.union(self.human_moves)))
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
		# if self.computer_turn == True:
		cell = None
		if len(self.computer_moves) == 1:
			started_cell = list(self.computer_moves)[0]
			opponent_cell = list(self.human_moves)[0]
			index_corner = self.corners.index(started_cell)
			
			# corners are either on the first column or last column
			if started_cell is not None and opponent_cell is not None:
				# if the opponent choose the center cell, the winning is not guaranteed
				# most likely it'll be a tie
				if opponent_cell == 5:
					cell = self.corners[len(self.corners) - 1 - index_corner]
				else:
					# the opponent picked any cell other than the center one
					# we could win the game by choosing another corner and creating a fork
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

		return cell

if __name__ == "__main__":
	ttt = Game()
	ttt.start()
