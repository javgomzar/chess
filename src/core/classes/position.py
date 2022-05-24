from dataclasses import dataclass
from string import ascii_lowercase
from .error_classes.errors import PositionError, VectorError
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


class Position(Vector):
    def __init__(self, col: int, row: int):
        if 0 <= min(row,col) and max(row,col) <= 7:
                self.col = col
                self.row = row
        else:
            raise PositionError(f"Row and col must be between 0 and 7")

    def __repr__(self):
        return f"<{self.__class__.__name__} object : ({self.col}, {self.row}), '{self.__str__()}'>"

    def __str__(self):
        return ascii_lowercase[0:8][self.col] + str(self.row + 1)

    def __hash__(self):
        return 8*self.col + self.row

    def __add__(self, other):
        if isinstance(other, Vector):
            return Position(self.col + other.col, self.row + other.row)
        else:
            raise TypeError(f"Can't add a Position to a {other.__class__}")

    @classmethod
    def from_notation(cls, notation: str):
        try:
            col = ascii_lowercase[0:8].index(notation[0])
            row = int(notation[1]) - 1
        except:
            raise PositionError(f"Can't initialize position with argument {notation}. Try with a letter between a-h and a number between 1-8, for example 'e4'")
        return cls(col,row)
