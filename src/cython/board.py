import platform
import importlib

name = 'cython._genpyx_' + '_'.join(platform.architecture()) + '_chess0x88'
try:
    chess = importlib.import_module(name)
    Board = chess.Board
    Move = chess.Move
    move_key = chess.move_key
except:
    print("Python Fallback. You may want to run on cython folder:")
    print("python setup.py build_ext --inplace")
    from chess0x88 import Board, Move, move_key