import sys
sys.path.append(sys.path[0] + '\\..')


import unittest as ut
from src.core.classes.position import *
from src.core.classes.color import *
from src.core.classes.board.board import *
from src.core.classes.pieces import *
from src.core.classes.ply import *
from src.core.classes.actions.action_controller import *
from src.core.classes.game import *
from src.core.classes.game_modes.standard import Standard
from src.core.classes.board_view import TextView, PygameView
from src.core.classes.players import BatchPlayer


class TestChess(ut.TestCase):
    white_player: BatchPlayer = BatchPlayer(White(),[
            Ply(White(), Position.from_notation('f2'), Position.from_notation('f4')),
            Ply(White(), Position.from_notation('f4'), Position.from_notation('f5')),
            Ply(White(), Position.from_notation('f5'), Position.from_notation('f6')),
            Ply(White(), Position.from_notation('f6'), Position.from_notation('g7')),
            Ply(White(), Position.from_notation('g7'), Position.from_notation('h8')),
            Ply(White(), Position.from_notation('h8'), Position.from_notation('g8')),
            Ply(White(), Position.from_notation('d2'), Position.from_notation('d4')),
            Ply(White(), Position.from_notation('c1'), Position.from_notation('h6')),
            Ply(White(), Position.from_notation('g8'), Position.from_notation('f8'))
        ])
    black_player: BatchPlayer = BatchPlayer(Black(),[
            Ply(Black(), Position.from_notation('a7'), Position.from_notation('a5')),
            Ply(Black(), Position.from_notation('b7'), Position.from_notation('b5')),
            Ply(Black(), Position.from_notation('a5'), Position.from_notation('a4')),
            Ply(Black(), Position.from_notation('a4'), Position.from_notation('a3')),
            Ply(Black(), Position.from_notation('a3'), Position.from_notation('b2')),
            Ply(Black(), Position.from_notation('b2'), Position.from_notation('a1')),
            Ply(Black(), Position.from_notation('a1'), Position.from_notation('b1')),
            Ply(Black(), Position.from_notation('b8'), Position.from_notation('c6'))
        ])

    def test_text_view(self):
        """Text view"""
        game = Game(Standard(), TextView(), self.white_player, self.black_player)
        game.main_loop()
        self.assertTrue(game.is_finished)
        self.white_player.reset()
        self.black_player.reset()

    def test_pygame_view(self):
        """Pygame view"""
        game = Game(Standard(), PygameView(2000), self.white_player, self.black_player)
        game.main_loop()
        self.assertTrue(game.is_finished)
        self.white_player.reset()
        self.black_player.reset()



if __name__ == '__main__':
    ut.main()
