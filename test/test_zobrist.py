import sys
sys.path.append(sys.path[0] + '\\..')

import unittest as ut
from src.core.classes.board.zobrist import *

class TestChess(ut.TestCase):

    def test_xor(self):
        for i in range(0,10):
            byte1 = rng.integers(32)
            byte2 = rng.integers(32)
            print(f"{byte1:b}, {byte2:b}")
            print(f'byte1: {int.from_bytes(chr(byte1), sys.byteorder)}')
            print(f'byte2: {int.from_bytes(chr(byte2), sys.byteorder)}')


if __name__ == '__main__':
    ut.main()
