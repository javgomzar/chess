from src.core.classes.color import Black, White
from src.core.classes.position import Vector
from src.core.classes.pieces.piece import Piece


class Knight(Piece):
    move_vectors = [Vector(sign_row*row, sign_col*col) for sign_row in [1,-1] for sign_col in [1,-1] for row,col in [(1,2),(2,1)]]
    image_file = "Knight.png"
    unicode = {
        Black(): '\u265E',
        White(): '\u2658'
    }

    def can_move(self, vector: Vector) -> bool:
        vector = abs(vector)
        return vector.col * vector.row == 2
