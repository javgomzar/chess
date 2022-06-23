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
from src.core.classes.players import *
from src.core.classes.board_view import *


class TestInput(ut.TestCase):
    def test_terminal_player(self):
        game = Game(Standard(), TextView(Standard()),AdvancedTerminalPlayer(White()), AdvancedTerminalPlayer(Black()))
        game.main_loop()

    def test_pygame(self):
        game = Game(Standard(), PygameView(Standard()), PygamePlayer(White()),PygamePlayer(Black()))
        game.main_loop()


if __name__ == '__main__':
    ut.main()
