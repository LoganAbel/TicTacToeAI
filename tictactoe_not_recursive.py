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
			for i in range(0,3)
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
	def predicted_results(this):
		def append_moves(i, tree):
			games, scores, move_lens, p_is = tree
			moves = [*games[i].moves()]
			games[:0] += moves
			scores[:0] += [move.results() for move in moves]
			move_lens[:0] += [len(moves)]
			p_is[:0] += [i+move_lens[0]]

		def delete_moves(tree):
			games, scores, move_lens, p_is = tree
			del scores[:move_lens[0]]
			del games[:move_lens[0]]
			del move_lens[0]
			del p_is[0]

		games = [this]
		scores = [None]
		move_lens = []
		p_is = []
		tree = [games, scores, move_lens, p_is]
		append_moves(0, tree)

		while None in scores:
			move_scores = scores[:move_lens[0]]
			p_i = p_is[0]
			p_turn = games[p_i].turn

			scores[p_i] = p_turn if p_turn in move_scores\
					else 0 if len(move_lens) > 2 and 0 in move_scores and 0 in scores[move_lens[0]:move_lens[1]]\
					else (0 if 0 in move_scores else -p_turn) if None not in move_scores\
					else None

			if scores[p_i] != None:
				delete_moves(tree)
			else:
				append_moves(move_scores.index(None), tree)

		return scores[0]

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
