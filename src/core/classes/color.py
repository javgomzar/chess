from src.core.classes.position import Position, Vector
from src.config.constants import MEDIA_PATH
from src.core.abstract_classes.singleton import Singleton


class Color(metaclass=Singleton):
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object>"


class Black(Color):
    image_folder_path = MEDIA_PATH + "Black/"
    pawn_row = 6
    king_row = 7
    pawn_direction = Vector(0,-1)
    king_position = Position(4, 7)

    def __str__(self):
        return "Black"

    def __int__(self):
        return 2

    def opposite_color(self):
        return White()


class White(Color):
    image_folder_path = MEDIA_PATH + "White/"
    pawn_row = 1
    king_row = 0
    pawn_direction = Vector(0,1)
    king_position = Position(4, 0)

    def __str__(self):
        return "White"

    def __int__(self):
        return 1

    def opposite_color(self):
        return Black()
