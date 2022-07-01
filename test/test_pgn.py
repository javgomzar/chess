import sys
sys.path.append(sys.path[0] + '\\..')

import unittest as ut

from src.core.classes.position import *
from src.core.classes.color import *
from src.core.classes.board import *
from src.core.classes.pieces import *
from src.core.classes.ply import *
from src.core.classes.game import *
from src.core.classes.game_modes import *
from src.core.classes.players import PGNPlayer
from src.core.classes.board_view import *


class TestInput(ut.TestCase):
    def test1(self):
        path = './games/game1.pgn'
        game = Game(Standard(), PygameView(Standard(), 1000), PGNPlayer(White(), path), PGNPlayer(Black(), path))
        game.main_loop()


if __name__ == '__main__':
    ut.main()
