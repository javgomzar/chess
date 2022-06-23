from ..vector import Vector
from .piece import Piece


rook_directions = [Vector(sign*vertical,sign*(1 - vertical)) for vertical in [0,1] for sign in [-1,1]]

class Rook(Piece):
    move_directions = rook_directions
    move_vectors = [step*direction for step in range(1,8) for direction in rook_directions]

    def __int__(self) -> int:
        return 4

    def can_move(self, vector: Vector) -> bool:
        vector = abs(vector)
        return vector.col * vector.row == 0 and vector.col + vector.row != 0