from ..actions import Action, Promote
from ..position import Position, Vector
from .action_rule import ActionRule
from ..pieces import Pawn
from ..ply import Ply
from ..board import Board

class PromoteRule(ActionRule):
    def validate(self, ply: Ply, board: Board) -> bool:
        piece = ply.piece
        if isinstance(piece, Pawn) and ply.to_position.row == ply.color.opposite_color().king_row:
            return not (piece.is_capture(ply.piece) ^ ply.taken_piece)

    def get_action(self, ply: Ply, board: Board) -> Action:
        return Promote(ply.piece, ply.vector)
