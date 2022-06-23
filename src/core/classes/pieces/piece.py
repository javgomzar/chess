from abc import ABC, abstractmethod

from ..color import Color
from ..position import Position
from ..error_classes import PositionError
from ..vector import Vector


class Piece(ABC):
    color : Color
    has_moved : bool
    move_vectors : list[Vector]

    def __init__(self, color: Color, has_moved : bool = False) -> None:
        self.color = color
        self.has_moved = has_moved

    def __repr__(self):
        return f"<{self.__class__.__name__} object : color={self.color}>"

    def __hash__(self):
        try:
            return self.id
        except:
            return id(self)

    def __eq__(self, other) -> None:
        try:
            return self.id == other.id
        except:
            return id(self) == id(other)

    def available_positions(self, from_position: Position) -> list[Position]:
        positions = []
        for vector in self.move_vectors:
            try:
                if self.can_move(vector):
                    positions.append(from_position + vector)
            except PositionError:
                pass
            except Exception as err:
                raise err
        return positions

    def copy(self):
        copied_self = self.__class__(self.color, self.has_moved)
        copied_self.id = self.id
        return copied_self

    @abstractmethod
    def can_move(self, vector: Vector) -> bool:
        pass
