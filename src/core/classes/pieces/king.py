from ..color import Black, White
from src.core.classes.position import Vector
from .piece import Piece


class King(Piece):
    move_vectors = [Vector(x,y) for x in [-1,0,1] for y in [-1,0,1] if x != 0 or y != 0] + [Vector(2,0), Vector(-2,0)]

    def __int__(self) -> int:
        return 0

    def can_move(self, vector: Vector) -> bool:
        vector = abs(vector)
        return max(vector.col, vector.row) == 1 and vector.col + vector.row != 0 or \
               self.is_castle(vector)

    def is_castle(self, vector: Vector) -> bool:
        return not self.has_moved and abs(vector) == Vector(2,0)
