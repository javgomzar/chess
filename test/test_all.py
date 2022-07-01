import sys
sys.path.append(sys.path[0] + '\\..')

import unittest as ut

from src.core.classes.error_classes import *
from src.core.classes.position import *
from src.core.classes.color import *
from src.core.classes.pieces import *
from src.core.classes.board import *


class TestChess(ut.TestCase):

    def test_checks(self):
        pass

    def test_pins(self):
        pass

    def test_blocks(self):
        pass

    def test_en_passant(self):
        pass

    def test_game(self):
        pass



if __name__ == '__main__':
    ut.main()
