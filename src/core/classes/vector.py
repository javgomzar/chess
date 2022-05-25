from dataclasses import dataclass
from .error_classes.errors import VectorError
from src.utils import sign

@dataclass
class Vector:
    col : int
    row: int

    def __init__(self, col: int, row: int):
        if -7 <= min(col,row) and max(col,row) <= 7:
            self.col = col
            self.row = row
        else:
            raise VectorError()

    def __str__(self):
        return f"({self.col}, {self.row})"

    def __abs__(self):
        return Vector(abs(self.col), abs(self.row))

    def __neg__(self):
        return Vector(-self.col, -self.row)

    def __eq__(self, other):
        try:
            other.col
            other.row
        except Exception:
            return False
        else:
            return self.col == other.col and self.row == other.row

    def __add__(self, other):
        return Vector(self.col + other.col, self.row + other.row)

    def __sub__(self, other):
        return Vector(self.col - other.col, self.row - other.row)

    def __mul__(self, other: int):
        return Vector(other * self.col, other * self.row)

    def __rmul__(self, other: int):
        return Vector(other * self.col, other * self.row)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : ({self.col}, {self.row})>"

    def normalize(self):
        return Vector(sign(self.col), sign(self.row))
