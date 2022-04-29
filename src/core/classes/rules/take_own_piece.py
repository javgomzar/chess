from ..board import Board
from ..ply import Ply
from .rule import Rule


class TakeOwnPiece(Rule):
    def validate(self, ply: Ply, board: Board) -> None:
        taken_piece = board.get_piece(ply.to_position)
        if taken_piece and taken_piece.color == ply.color:
            return False
        else:
            ply.taken_piece = taken_piece
            return True
