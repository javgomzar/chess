from .action_rule import ActionRule
from ..actions import Action, Move
from ..ply import Ply
from ..board import Board
from ..pieces import Pawn


class MoveRule(ActionRule):
    def validate(self, ply: Ply, board: Board) -> bool:
        piece = ply.piece
        if isinstance(piece, Pawn):
            return not (piece.is_capture(ply.vector) ^ bool(ply.taken_piece))
        return True

    def get_action(self, ply: Ply) -> Action:
        return Move(ply.piece, ply.vector)
    