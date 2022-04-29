from ..actions import Action, Castle
from ..position import Position, Vector
from .action_rule import ActionRule
from ..pieces import King, Rook
from ..ply import Ply
from ..board import Board



class CastleRule(ActionRule):
    def validate(self, ply: Ply, board: Board) -> bool:
        piece = ply.piece
        if isinstance(piece, King) and piece.is_castle(ply.vector):
            direction = ply.vector.normalize()
            rook_col = 0 if direction == Vector(-1,0) else 7
            rook = board.get_piece(Position(rook_col, ply.color.king_row))
            if rook and isinstance(rook, Rook) and not rook.has_moved:
                return True
        return False

    def get_action(sel, ply: Ply) -> Action:
        return Castle(ply.color, ply.vector.normalize())
