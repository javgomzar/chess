from dataclasses import dataclass
from string import ascii_lowercase
from src.core.error_classes.errors import PositionError, VectorError

@dataclass
class Vector:
    col : int
    row: int

    def __init__(self, col: int, row: int) -> None:
        if -7 <= min(col,row) and max(col,row) <= 7:
            self.col = col
            self.row = row
        else:
            raise VectorError()

    def __hash__(self):
        return (self.col, self.row).__hash__()

    def __str__(self):
        return f"({self.col}, {self.row})"

    def __abs__(self):
        return Vector(abs(self.col), abs(self.row))

    def __neg__(self):
        return Vector(-self.col, -self.row)

    def __eq__(self, other):
        return self.col == other.col and self.row == other.row

    def __add__(self, other):
        return Vector(self.col + other.col, self.row + other.row)

    def __sub__(self, other):
        return Vector(self.col - other.col, self.row - other.row)

    def __mul__(self, other: int):
        return Vector(other * self.col, other * self.row)

    def __rmul__(self, other: int):
        return Vector(other * self.col, other * self.row)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object : ({self.col}, {self.row})>"


class Position(Vector):
    def __init__(self, col: int, row: int) -> None:
        if 0 <= min(row,col) and max(row,col) <= 7:
            self.col = col
            self.row = row
        else:
            raise PositionError()

    def __str__(self):
        return ascii_lowercase[0:8][self.col] + str(self.row + 1)

    def __add__(self, other):
        return Position(self.col + other.col, self.row + other.row)
