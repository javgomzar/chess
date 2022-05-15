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
from src.core.classes.error_classes.errors import InvalidMove
from src.core.classes.game_modes.standard import Standard
from src.core.classes.players.batch_player import BatchPlayer

class TestChess(ut.TestCase):
    def test_game1(self):
        """Quick mate"""
        print("\nGame 1:\n")
        game = Game(Standard(), 
        BatchPlayer(White(),[
            Ply(White(), Position.from_notation('e2'), Position.from_notation('e4')),
            Ply(White(), Position.from_notation('f1'), Position.from_notation('c4')),
            Ply(White(), Position.from_notation('d1'), Position.from_notation('f3')),
            Ply(White(), Position.from_notation('f3'), Position.from_notation('f7'))
        ]),
        BatchPlayer(Black(),[
            Ply(Black(), Position.from_notation('a7'), Position.from_notation('a6')),
            Ply(Black(), Position.from_notation('a6'), Position.from_notation('a5')),
            Ply(Black(), Position.from_notation('a5'), Position.from_notation('a4'))
        ]))
        game.main_loop()
        self.assertTrue(game.is_finished)

    def test_game2(self):
        """Repetition tie"""
        print("\nGame 2: \n")
        game = Game(Standard(), 
        BatchPlayer(White(),[
            Ply(White(), Position.from_notation('g1'), Position.from_notation('f3')),
            Ply(White(), Position.from_notation('f3'), Position.from_notation('g1')),
            Ply(White(), Position.from_notation('g1'), Position.from_notation('f3')),
            Ply(White(), Position.from_notation('f3'), Position.from_notation('g1')),
            Ply(White(), Position.from_notation('g1'), Position.from_notation('f3')),
            Ply(White(), Position.from_notation('f3'), Position.from_notation('g1'))
        ]),
        BatchPlayer(Black(),[
            Ply(Black(), Position.from_notation('g8'), Position.from_notation('f6')),
            Ply(Black(), Position.from_notation('f6'), Position.from_notation('g8')),
            Ply(Black(), Position.from_notation('g8'), Position.from_notation('f6')),
            Ply(Black(), Position.from_notation('f6'), Position.from_notation('g8')),
            Ply(Black(), Position.from_notation('g8'), Position.from_notation('f6')),
            Ply(Black(), Position.from_notation('f6'), Position.from_notation('g8'))
        ]))
        game.main_loop()
        self.assertTrue(game.is_finished and isinstance(game.final_state, Draw))

    def test_game3(self):
        """Testing castling checks"""
        print("\nGame 3: \n")
        game = Game(Standard(), 
        BatchPlayer(White(),[
            Ply(White(), Position.from_notation('e2'), Position.from_notation('e4')),
            Ply(White(), Position.from_notation('f1'), Position.from_notation('b5')),
            Ply(White(), Position.from_notation('f2'), Position.from_notation('f4')),
            Ply(White(), Position.from_notation('g1'), Position.from_notation('f3')),
            Ply(White(), Position.from_notation('e1'), Position.from_notation('g1'))
        ]),
        BatchPlayer(Black(),[
            Ply(Black(), Position.from_notation('d7'), Position.from_notation('d5')),
            Ply(Black(), Position.from_notation('c8'), Position.from_notation('d7')),
            Ply(Black(), Position.from_notation('d7'), Position.from_notation('b5')),
            Ply(Black(), Position.from_notation('a7'), Position.from_notation('a5'))
        ]))
        self.assertRaises(InvalidMove, game.main_loop)

    def test_game4(self):
        """Testing pawn promotion"""
        print("\nGame 4: \n")
        game = Game(Standard(), 
        BatchPlayer(White(),[
            Ply(White(), Position.from_notation('f2'), Position.from_notation('f4')),
            Ply(White(), Position.from_notation('f4'), Position.from_notation('f5')),
            Ply(White(), Position.from_notation('f5'), Position.from_notation('f6')),
            Ply(White(), Position.from_notation('f6'), Position.from_notation('g7')),
            Ply(White(), Position.from_notation('g7'), Position.from_notation('h8')),
            Ply(White(), Position.from_notation('h8'), Position.from_notation('g8')),
            Ply(White(), Position.from_notation('d2'), Position.from_notation('d4')),
            Ply(White(), Position.from_notation('c1'), Position.from_notation('h6')),
            Ply(White(), Position.from_notation('g8'), Position.from_notation('f8'))
        ]),
        BatchPlayer(Black(),[
            Ply(Black(), Position.from_notation('a7'), Position.from_notation('a5')),
            Ply(Black(), Position.from_notation('b7'), Position.from_notation('b5')),
            Ply(Black(), Position.from_notation('a5'), Position.from_notation('a4')),
            Ply(Black(), Position.from_notation('a4'), Position.from_notation('a3')),
            Ply(Black(), Position.from_notation('a3'), Position.from_notation('b2')),
            Ply(Black(), Position.from_notation('b2'), Position.from_notation('a1')),
            Ply(Black(), Position.from_notation('a1'), Position.from_notation('b1')),
            Ply(Black(), Position.from_notation('b8'), Position.from_notation('c6'))
        ]))
        game.main_loop()
        self.assertTrue(game.is_finished and isinstance(game.final_state, Win))



if __name__ == '__main__':
    ut.main()
