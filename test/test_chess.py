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
        for color in [Black(), White()]:
            for position in [Position(col,row) for col in range(0,8) for row in range(0,8)]:
                for is_active in [True, False]:
                    for has_moved in [True, False]:
                        # Pawn tests
                        pawn = Pawn(color, position, is_active, has_moved)
                        self.assertTrue(pawn == pawn.copy(), "Pawn copying is failing")
                        if position.row == color.pawn_row and not has_moved:
                            self.assertTrue(pawn.can_move(position + 2*color.pawn_direction), "Pawn first move check is failing")
                        try:
                            to_position = position + color.pawn_direction
                        except PositionError:
                            pass
                        else:
                            self.assertTrue(pawn.can_move(to_position), "Pawn move is failing")
                        for col_delta in [-1,1]:
                            try:
                                to_position = position + Vector(col_delta, color.pawn_direction.row)
                            except PositionError:
                                pass
                            else:
                                self.assertTrue(pawn.can_move(to_position), "Pawn capture check is failing")
                        
                        for piece_class in [Bishop, Rook, Queen]:
                            pass


    def test_board(self):
        board = Board()
        for color in [Black(), White()]:
            for col,piece_class in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
                pawn = board.get_piece(Position(col,color.pawn_row))
                self.assertTrue(isinstance(pawn, Pawn),"Pawn check is failing.")
                piece = board.get_piece(Position(col,color.king_row))
                self.assertTrue(isinstance(piece, piece_class),"Not pawns check is failing.")
                self.assertTrue(pawn in board and piece in board, "__contains__ is failing")
                try:
                    board.pieces.remove(pawn)
                    board.pieces.remove(piece)
                except Exception() as err:
                    raise err
                self.assertFalse(pawn in board and piece in board, "remove is failing")
                board.pieces.append(pawn)
                board.pieces.append(piece)

        self.assertEqual(board.get_king(Black()).position, Position(4,7), "get_king_position is failing for black")
        self.assertEqual(board.get_king(White()).position, Position(4,0), "get_king_position is failing for white")
        copied_board = board.copy()
        self.assertTrue(board == copied_board, "board copy or __eq__ is failing")

    def test_controller(self):
        controller = BoardController()

        white_pawn = controller.board.get_piece(Position(4,1))
        black_pawn = controller.board.get_piece(Position(3,6))
        black_knight = controller.board.get_piece(Position(6,7))
        black_queen = controller.board.get_piece(Position(3,7))

        controller.execute(Move(white_pawn, Position(4,3))),
        controller.execute(Move(black_knight, Position(5,5))),
        controller.execute(Move(white_pawn, Position(4,4))),
        controller.execute(Move(black_pawn, Position(3,4))),
        controller.execute(EnPassant(white_pawn, Position(3,5))),
        controller.execute(Move(black_queen, Position(3,5)))

        print(controller.board)
        for action in reversed(controller.undo_stack):
            print(action)
            controller.undo()
            print(controller.board)

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
