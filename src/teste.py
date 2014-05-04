from cython.board import Board

board = Board(new_game=True)
#board.load_fen("8/8/8/4N3/8/8/8/8 w kQkq - 0 1")
print(board.count(1, 1))
board.display()
