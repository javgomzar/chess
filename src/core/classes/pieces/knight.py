from ..vector import Vector
from .piece import Piece


class Knight(Piece):
    move_vectors = [Vector(sign_row*row, sign_col*col) for sign_row in [1,-1] for sign_col in [1,-1] for row,col in [(1,2),(2,1)]]

    def __int__(self):
        return 2

    def can_move(self, vector: Vector) -> bool:
        vector = abs(vector)
        return vector.col * vector.row == 2
