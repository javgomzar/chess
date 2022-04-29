from .final_states import FinalState, Win, Draw
from ..handler import Handler
from ..position import Vector
from ..pieces import Bishop, Knight, King, Pawn, Queen, Rook
from ..color import Color
from ..board import Board
from ..ply import Ply
from ..error_classes import PositionError

class Check(Handler):
    def condition(self, ply: Ply, board: Board) -> bool:
        ply.is_check = self.is_check(ply.color.opposite_color(), board)
        return ply.is_finished

    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        return Win() if ply.is_check else Draw()

    @classmethod
    def is_check(self, color: Color, board: Board) -> bool:
        """
        Checks if a board contains a check for the king of a given color.
        """
        king_position = board.get_king_position(color)

        # Knight checks... and king checks?
        for piece_class in [Knight, King]:
            for vector in piece_class.move_vectors:
                try:
                    pointer = king_position + vector
                except PositionError:
                    pass
                else:
                    piece = board.get_piece(pointer)
                    if piece and isinstance(piece, piece_class) and piece.color != color:
                        return True

        # Bishop and rook checks (and Queen)
        for piece_class in [Bishop, Rook]:
            for direction in piece_class.move_directions:
                pointer = king_position
                while True:
                    try:
                        pointer += direction
                    except PositionError:
                        break
                    else:
                        piece = board.get_piece(pointer)
                        if piece:
                            if piece.color == color:
                                break
                            elif isinstance(piece,piece_class) or isinstance(piece,Queen):
                                return True
                            else:
                                break

        # Pawn checks
        for direction in [color.pawn_direction + Vector(delta_col, 0) for delta_col in [-1,1]]:
            try:
                pointer = king_position + direction
            except PositionError:
                break
            piece = board.get_piece(pointer)
            if piece and isinstance(piece, Pawn) and piece.color != color:
                return True

        return False