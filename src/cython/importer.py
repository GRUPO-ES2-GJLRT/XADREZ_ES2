import platform
import importlib
from utils.pyx_replace import read_file


name = 'cython._genpyx_' + '_'.join(platform.architecture()) + '_chess0x88'
try:
    chess = importlib.import_module(name)
    checksum = chess.CHECKSUM
    expected_checksum = read_file("chess0x88.py", [], "cython")
    if checksum != expected_checksum:
        print("Invalid checksum.")
        raise Exception('checksum')
    Board = chess.Board
    Move = chess.Move
    move_key = chess.move_key
except Exception as e:
    print("Python Fallback. You may want to run on cython folder:")
    print("python setup.py build_ext --inplace")
    from chess0x88 import Board, Move, move_key
