from src.core.classes.color import Black, White
from src.core.classes.position import Vector
from src.core.classes.pieces.piece import Piece

rook_directions = [Vector(sign*vertical,sign*(1 - vertical)) for vertical in [0,1] for sign in [-1,1]]

class Rook(Piece):
    move_directions = rook_directions
    move_vectors = [step*direction for step in range(1,8) for direction in rook_directions]
    image_file = "Rook.png"
    unicode = {
        Black(): '\u265C',
        White(): '\u2656'
    }

    def __int__(self):
        return 4

    def can_move(self, vector: Vector) -> bool:
        vector = abs(vector)
        return vector.col * vector.row == 0 and vector.col + vector.row != 0