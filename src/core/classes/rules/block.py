from ..pieces import Knight
from ..ply import Ply
from ..board import Board

from .rule import Rule


class Block(Rule):
    """
    Checks if a ply is a movement blocked by other piece.
    """
    def process(self, ply: Ply, board: Board) -> None:
        return

    @classmethod
    def validate(self, ply: Ply, board: Board) -> bool:
        if not isinstance(ply.piece, Knight):
            direction = ply.vector.normalize()
            pointer = ply.from_position + direction
            while pointer != ply.to_position:
                if board.get_piece(pointer):
                    return False
                pointer += direction
        return True
