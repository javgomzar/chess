from .position import Position
from .vector import Vector
from src.core.metaclasses.singleton import Singleton


class Color(metaclass=Singleton):
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object>"


class Black(Color):
    pawn_row = 6
    king_row = 7
    pawn_direction = Vector(0,-1)
    king_position = Position(4, 7)

    def __str__(self):
        return "Black"

    def opposite_color(self):
        return White()


class White(Color):
    pawn_row = 1
    king_row = 0
    pawn_direction = Vector(0,1)
    king_position = Position(4, 0)

    def __str__(self):
        return "White"

    def opposite_color(self):
        return Black()
