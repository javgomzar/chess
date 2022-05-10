from ..board import Board
from ..ply import Ply
from .rule import Rule


class ValidPieceMove(Rule):
    def process(self, ply: Ply, board: Board) -> None:
        pass

    @classmethod
    def validate(self, ply: Ply, board: Board) -> bool:
        return ply.piece.can_move(ply.vector)
