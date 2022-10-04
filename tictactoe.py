class Game:
	def __init__(this, board=None, turn=None):
		this.board = board or [0,0,0,0,0,0,0,0,0]
		this.turn = turn or 1
	def __repr__(this):
		return '\n'.join(
			' '.join(
				'X' if v == 1 else 
				'O' if v == -1 else 
				'-' if v == 0 else v
				for v in this.board[3*i:3*i+3:]
			)
			for i in range(int(len(this.board)/3))
		)
	def __eq__(this, that):
		return any(tran.board == this.board for tran in that.transforms())
	def results(this):
		win_spots = [
			tuple(arr) for arr in
			[this.board[3*i:3*i+3:] for i in range(0,3)] + [this.board[i:i+9:3] for i in range(0,3)] + [this.board[::4], this.board[2:7:2]]
		]
		return 1 if (1,1,1) in win_spots else -1 if (-1,-1,-1) in win_spots else None if any(v == 0 for v in this.board) else 0
	def moves(this):
		for i,v in enumerate(this.board):
			if v == 0:
				yield this.move(i)
	def move(this, i):
		board = [*this.board]
		if board[i] == 0:
			board[i] = this.turn
			return Game(board, -this.turn)
		else:
			turn = board[i]
			board[i] = 0
			return Game(board, turn)
	def is_loss(this):
		results = this.results()
		if results in (-this.turn, 0):
			return False
		if results == this.turn:
			return True
	def is_win(this):
		results = this.results()
		if results in (this.turn, 0):
			return False
		if results == -this.turn:
			return True

	def predict_loss(this):
		loss = this.is_loss()
		if loss != None: return loss
		return any(move.predict_win() for move in this.moves())
	def predict_win(this):
		win = this.is_win()
		if win != None: return win
		return all(move.predict_loss() for move in this.moves())
	def predicted_results(this):
		results = this.results()
		if results != None:
			return results

		moves = this.moves()
		for move in moves:
			results = move.predicted_results()
			if results == this.turn:
				return this.turn
			if results == 0:
				return this.turn if any(move.predict_win() for move in moves) else 0
		return -this.turn

	def square_results(this):
		return Game([this.move(i).predicted_results() if this.board[i] == 0 else ' ' for i in range(9)])

def str_wrap(games, width):
	return '\n\n'.join(inline_str(games[i:i+width])for i in range(0,len(games),width))

def get_axis():
	return keyboard.is_pressed('right arrow') - keyboard.is_pressed('left arrow'), \
		   keyboard.is_pressed('down arrow') - keyboard.is_pressed('up arrow')

import os
import keyboard

game = Game()
results = game.square_results()
x,y = 0,0
while 1:
	os.system('cls')
	pointer = [[' ',' ',' '] for i in range(3)]
	pointer[y][x] = '^'

	print()
	print(' '+'\n '.join(row1.replace(' ', '  ') + '\n ' + '  '.join(p for p in row2) for row1, row2 in zip(str(game).split('\n'), pointer)))
	print()
	print('  score')
	print('  '+str(results).replace('\n','\n  '))
	print()

	while get_axis() != (0,0) or keyboard.is_pressed('enter'): pass
	while 1:
		dx, dy = get_axis()
		if (dx != 0 and 0 <= x+dx < 3) or (dy != 0 and 0 <= y+dy < 3):
			x += dx
			y += dy
			break
		if keyboard.is_pressed('enter'):
			game = game.move(y*3+x)
			results = game.square_results()
			break