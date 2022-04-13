import unittest as ut
from os.path import isdir
import sys
sys.path.append(sys.path[0] + '\\..')

from src.core.classes.position import *
from src.core.classes.color import *
from src.core.classes.board import *
from src.core.classes.pieces import *
from src.core.classes.actions import *
from src.core.classes.board_controller import *
from src.core.classes.game import *

class TestChess(ut.TestCase):
    def test_vector(self):
        for col,row in [(col,row) for col in range(-10,10) for row in range(-10,10)]:
            if -7 > min(col,row) or max(col,row) > 7:
                self.assertRaises(VectorError, lambda: Vector(col,row))

    def test_position(self):
        for col,row in [(col,row) for col in range(-10,10) for row in range(-10,10)]:
            if 0 > min(col,row) or max(col,row) > 7:
                self.assertRaises(PositionError, lambda: Position(col,row))

    def test_color(self):
        white = White()
        black = Black()

        self.assertTrue(white != black and white == White() and black == Black(), "Color __eq__ is failing.")
        self.assertTrue(isdir(white.image_folder_path) and isdir(black.image_folder_path), "Image folder paths not found.")
        self.assertTrue(white.pawn_row == 1 and black.pawn_row == 6)
        self.assertTrue(white.king_row == 0 and black.king_row == 7)
        self.assertTrue(white.pawn_direction == Vector(0,1) and black.pawn_direction == Vector(0,-1))
        self.assertTrue(white.king_position == Position(4,0) and black.king_position == Position(4,7))

    def test_piece(self):
        for color in [Black(), White()]:
            for position in [Position(col,row) for col in range(0,8) for row in range(0,8)]:
                for has_moved in [True, False]:
                    # Pawn tests
                    pawn = Pawn(color, has_moved)
                    # self.assertTrue(pawn == pawn.copy(), "Pawn copying is failing")
                    if position.row == color.pawn_row and not has_moved:
                        self.assertTrue(pawn.can_move(2*color.pawn_direction), "Pawn first move check is failing")
                    try:
                        to_position = position + color.pawn_direction
                    except PositionError:
                        pass
                    else:
                        self.assertTrue(pawn.can_move(to_position - position), "Pawn move is failing")
                    for col_delta in [-1,1]:
                        try:
                            to_position = position + Vector(col_delta, color.pawn_direction.row)
                        except PositionError:
                            pass
                        else:
                            self.assertTrue(pawn.is_capture(to_position - position), "Pawn capture check is failing")
                    
                    for piece_class in [Bishop, Rook, Queen]:
                        pass

    def test_board(self):
        board = Board()
        for color in [Black(), White()]:
            for col,piece_class in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
                pawn_position = Position(col,color.pawn_row)
                pawn = board.get_piece(pawn_position)
                self.assertTrue(isinstance(pawn, Pawn),"Pawn check is failing.")
                piece_position = Position(col,color.king_row)
                piece = board.get_piece(piece_position)
                self.assertTrue(isinstance(piece, piece_class),"Not pawns check is failing.")
                self.assertTrue(pawn in board and piece in board, "__contains__ is failing")
                try:
                    board.remove(pawn)
                    board.remove(piece)
                except Exception as err:
                    raise err
                self.assertTrue(board.get_position(pawn) == None and board.get_position(piece) == None, "remove is failing")
                board.set_position(pawn, pawn_position)
                board.set_position(piece, piece_position)

        black_king_position = board.get_king_position(Black())
        self.assertEqual(black_king_position, Position(4,7), "get_king_position is failing for black")
        white_king_position = board.get_king_position(White())
        self.assertEqual(white_king_position, Position(4,0), "get_king_position is failing for white")
        # copied_board = board.copy()
        # self.assertTrue(len(copied_board.positions) == len(board.positions))
        # for piece in board:
        #     self.assertTrue(piece in copied_board)

    # def test_controller(self):
    #     controller = BoardController()

    #     white_pawn = controller.board.get_piece(Position(4,1))
    #     black_pawn = controller.board.get_piece(Position(3,6))
    #     black_knight = controller.board.get_piece(Position(6,7))

    #     controller.execute(Move(white_pawn, Vector(0,2)))
    #     controller.execute(Move(black_knight, Vector(-1,2)))
    #     controller.execute(Move(white_pawn, Vector(0,1)))
    #     controller.execute(Move(black_pawn, Vector(0,-2)))
    #     controller.execute(EnPassant(white_pawn, Vector(-1,1)))


    #     print(controller.board)
    #     for action in reversed(controller.undo_stack):
    #         print(controller.get_previous_board())
    #         controller.undo()
    #         print(controller.board)

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
