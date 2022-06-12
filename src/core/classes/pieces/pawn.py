from src.core.classes.error_classes.errors import PositionError
from ..color import Color, Black, White
from src.core.classes.position import Vector
from .piece import Piece
from ..position import Position, Vector


class Pawn(Piece):
    def __init__(self, color: Color, has_moved : bool = False) -> None:
        super().__init__(color, has_moved)
        self.move_vectors = [step*color.pawn_direction for step in [1,2]] + \
                            [Vector(delta_col, color.pawn_direction.row) for delta_col in [1,-1]]

    def __int__(self) -> int:
        return 1

    def can_move(self, vector: Vector) -> bool:
        return abs(vector.col) == 1 and vector.row == self.color.pawn_direction.row or \
               abs(vector.col) == 0 and (vector.row == self.color.pawn_direction.row or
               not self.has_moved and vector.row == 2*self.color.pawn_direction.row)

    def is_capture(self, vector: Vector) -> bool:
        return abs(vector.col) == 1 and vector.row == self.color.pawn_direction.row

    def available_captures(self, from_position: Position) -> list[Position]:
        result = []
        for vector in [Vector(-1,0), Vector(1,0)]:
            try:
                position = from_position + self.color.pawn_direction + vector
            except PositionError:
                pass
            else:
                result.append(position)
        return result
