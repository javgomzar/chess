from src.core.classes.color import Color, Black, White
from src.core.classes.position import Vector
from src.core.classes.pieces.piece import Piece


class Pawn(Piece):
    image_file = "Pawn.png"
    unicode = {
        Black(): '\u265F',
        White(): '\u2659'
    }

    def __init__(self, color: Color, has_moved : bool = False) -> None:
        super().__init__(color, has_moved)
        self.move_vectors = [step*color.pawn_direction for step in [1,2]] + \
                            [Vector(delta_col, color.pawn_direction.row) for delta_col in [1,-1]]

    def __int__(self):
        return int(self.color)

    def can_move(self, vector: Vector) -> bool:
        return abs(vector.col) == 1 and vector.row == self.color.pawn_direction.row or \
               abs(vector.col) == 0 and (vector.row == self.color.pawn_direction.row or
               not self.has_moved and vector.row == 2*self.color.pawn_direction.row)

    def is_capture(self, vector: Vector):
        return abs(vector.col) == 1 and vector.row == self.color.pawn_direction.row