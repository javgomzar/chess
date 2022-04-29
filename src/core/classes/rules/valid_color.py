from ..pieces import Pawn
from ..board import Board
from ..ply import Ply
from .rule import Rule


class ValidColor(Rule):
    def validate(self, ply: Ply, board: Board) -> bool:
        piece = board.get_piece(ply.from_position)
        ply.piece = piece
        return piece and ply.color == piece.color
