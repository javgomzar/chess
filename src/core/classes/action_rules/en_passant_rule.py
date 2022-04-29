from ..color import Black
from .action_rule import ActionRule
from ..actions import Action, EnPassant
from ..position import Position
from ..pieces import Pawn
from ..ply import Ply
from ..board import Board


class EnPassantRule(ActionRule):
    def validate(self, ply: Ply, board: Board) -> bool:
        """
        Checks if a ply is an "en passant" move.
        """
        if Pawn(ply.color).is_capture(ply.vector) and not ply.taken_piece:
            passed_pawn_position = ply.to_position + (-ply.color.pawn_direction)
            passed_pawn = board.get_piece(passed_pawn_position)
            previous_board = board.get_previous_board()
            previous_pawn_position = Position(ply.to_position.col, ply.color.opposite_color().pawn_row)
            previous_pawn = previous_board.get_piece(previous_pawn_position)
            return previous_pawn and passed_pawn and previous_pawn == passed_pawn and \
                   ply.from_position.row == (3 if ply.color == Black() else 4)

    def get_action(self, ply: Ply) -> Action:
        return EnPassant(ply.piece, ply.to_position)