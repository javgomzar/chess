from ..board import Board
from ..ply import Ply
from .rule import Rule


class TakeOwnPiece(Rule):
    def process(self, ply: Ply, board: Board) -> None:
        taken_piece = board.get_piece(ply.to_position)
        ply.taken_piece = taken_piece

    def validate(self, ply: Ply, board: Board) -> None:
        if ply.taken_piece and ply.taken_piece.color == ply.color:
            return False
        else:
            return True
