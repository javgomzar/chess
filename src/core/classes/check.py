from .position import Vector, Position
from .pieces import Bishop, Knight, King, Pawn, Queen, Rook
from .color import Color
from .board import Board
from .error_classes import PositionError


class Check:
    @classmethod
    def is_check(color: Color, board: Board) -> bool:
        """
        Checks if a board contains a check for the king of a given color.
        """
        king_position = board.get_king_position(color)

        # Knight and king checks
        if Check.knight_and_king_checks(color, board, king_position)

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

    @classmethod
    def knight_and_king_checks(color: Color, board: Board, king_position: Position) -> bool:
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

    @classmethod
    def bishop_rook_and_queen_checks() -> bool:
        pass

    @classmethod
    def pawn_checks(self) -> bool:
        pass
