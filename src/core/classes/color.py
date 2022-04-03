
from src.core.classes.position import Vector
from src.config.constants import MEDIA_PATH
from src.core.metaclasses.Singleton import Singleton


class Color(metaclass=Singleton):
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object>"

class Black(Color):
    image_folder_path = MEDIA_PATH + "Black/"
    pawn_row_index = 6
    king_row_index = 7
    pawn_direction = Vector(0,-1)

    def __str__(self):
        return "Black"

    def opposite_color(self):
        return White()

class White(Color):
    image_folder_path = MEDIA_PATH + "White/"
    pawn_row_index = 1
    king_row_index = 0
    pawn_direction = Vector(0,1)

    def __str__(self):
        return "White"

    def opposite_color(self):
        return Black()
