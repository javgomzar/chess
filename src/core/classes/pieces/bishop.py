from src.core.classes.color import Black, White
from src.core.classes.position import Vector
from src.core.classes.pieces.piece import Piece

bishop_directions = [Vector(x,y) for x in [1,-1] for y in [1,-1]]

class Bishop(Piece):
    move_directions = bishop_directions
    move_vectors = [step*direction for step in range(1,8) for direction in bishop_directions]
    image_file = "Bishop.png"
    unicode = {
        Black(): '\u265D',
        White(): '\u2657'
    }

    def can_move(self, vector: Vector) -> bool:
        vector = abs(vector)
        return vector.col == vector.row and vector.col != 0