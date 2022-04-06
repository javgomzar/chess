from src.core.classes.color import Color
from src.core.classes.position import Position, PositionError, Vector
from PIL import Image
from abc import ABC, abstractmethod


class Piece(ABC):
    move_vectors : list[Vector]
    image_path : str
    color : Color
    position : Position
    is_active : bool
    has_moved : bool

    def __init__(self, color: Color, position : Position, is_active : bool = True, has_moved : bool = False) -> None:
        self.color = color
        self.image_path = color.image_folder_path + self.image_file
        self.unicode = self.unicode[color]
        self.position = position
        self.is_active = is_active
        self.has_moved = has_moved

    def __str__(self) -> str:
        return self.unicode

    def __repr__(self):
        return f"<{self.__class__.__name__} object : color={self.color}, position={self.position}>"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.color == other.color and \
               self.position == other.position and \
               self.is_active == other.is_active and \
               self.has_moved == other.has_moved

    def image(self) -> Image:
        return Image.open(self.image_path)

    def copy(self):
        return self.__class__(self.color, self.position, self.is_active, self.has_moved)

    def available_positions(self) -> list[Position]:
        positions = []
        for vector in self.move_vectors:
            try:
                positions.append(self.position + vector)
            except PositionError:
                pass
            except Exception as err:
                raise err
        return positions

    @abstractmethod
    def can_move(self, to_position: Position) -> bool:
        pass
