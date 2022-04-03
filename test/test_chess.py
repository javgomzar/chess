import unittest as ut
import sys
sys.path.append(sys.path[0] + '\\..')

from src.core.classes.position import *
from src.core.classes.color import *
from src.core.classes.board import *
from src.core.classes.piece import *
from src.core.classes.actions import *
from src.core.classes.board_controller import *
from src.core.classes.game import *

class TestChess(ut.TestCase):
    def test_color(self):
        pass

    def test_position(self):
        pass

    def test_piece(self):
        pass

    def test_board(self):
        board = Board()
        for color in [Black(), White()]:
            for col,piece_class in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
                self.assertTrue(isinstance(board.get_piece(Position(col,color.pawn_row_index)), Pawn),"Pawn check is failing.")
                self.assertTrue(isinstance(board.get_piece(Position(col,color.king_row_index)), piece_class),"Not pawns check is failing.")

        self.assertEqual(board.get_king_position(Black()), Position(4,7), "get_king_position is failing for black")
        self.assertEqual(board.get_king_position(White()), Position(4,0), "get_king_position is failing for white")

        self.assertTrue(board == board.copy(), "board copy is failing")

    def test_controller(self):
        pass

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
