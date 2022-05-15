from ..actions import Action, Castle, Move
from ..position import Position, Vector
from .action_rule import ActionRule
from ..pieces import King, Rook
from ..ply import Ply
from ..board import Board
from ..finish_conditions import Check
from ..error_classes import InvalidMove


class CastleRule(ActionRule):
    def validate(self, ply: Ply, board: Board) -> bool:
        piece = ply.piece
        if isinstance(piece, King) and piece.is_castle(ply.vector):
            direction = ply.vector.normalize()
            rook_col = 0 if direction == Vector(-1,0) else 7
            rook = board.get_piece(Position(rook_col, ply.color.king_row))
            if rook and isinstance(rook, Rook) and not rook.has_moved:
                possible_board = board
                for i in range(0,2):
                    if Check.is_check(ply.color, possible_board):
                        break
                    possible_board = possible_board.try_action(Move(piece, direction))
                else:
                    return True
                raise InvalidMove()
        return False

    def get_action(sel, ply: Ply) -> Action:
        return Castle(ply.color, ply.vector.normalize())
