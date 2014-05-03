from chess0x88 import Board

board = Board(new_game=True)
#board.load_fen("8/8/8/4N3/8/8/8/8 w kQkq - 0 1")
board.display()
print(set(board.possible_moves("white")))
print(set(board.possible_moves("black")))
print(board.color())
board.display()