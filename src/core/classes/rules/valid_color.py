from ..pieces import Pawn
from ..board import Board
from ..ply import Ply

from .rule import Rule


class ValidColor(Rule):
    def process(self, ply: Ply, board: Board) -> None:
        ply.piece = board.get_piece(ply.from_position)

    def validate(self, ply: Ply, board: Board) -> bool:
        return ply.piece and ply.color == ply.piece.color
