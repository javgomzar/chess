from ..color import Black, White
from src.core.classes.position import Vector
from .piece import Piece

queen_directions = [Vector(x,y) for x in [1,-1] for y in [1,-1]] + \
                   [Vector(sign*vertical,sign*(1 - vertical)) for vertical in [0,1] for sign in [-1,1]]

class Queen(Piece):
    move_directions = queen_directions
    move_vectors = [step*vector for step in range(1,8) for vector in queen_directions]

    def __int__(self):
        return 5

    def can_move(self, vector: Vector) -> bool:
        vector = abs(vector)
        return vector.col * vector.row * (vector.col - vector.row) == 0 and vector.col + vector.row != 0
