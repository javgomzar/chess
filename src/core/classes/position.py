from dataclasses import dataclass
from string import ascii_lowercase
from src.core.error_classes.errors import PositionError, VectorError
from src.utils import sign

sixtyfour_primes = [  2,   3,   5,   7,  11,  13,  17,  19,
                     23,  29,  31,  37,  41,  43,  47,  53,
                     59,  61,  67,  71,  73,  79,  83,  89,
                     97, 101, 103, 107, 109, 113, 127, 131,
                    137, 139, 149, 151, 157, 163, 167, 173,
                    179, 181, 191, 193, 197, 199, 211, 223,
                    227, 229, 233, 239, 241, 251, 257, 263,
                    269, 271, 277, 281, 283, 293, 307, 311]

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

    # def __hash__(self):
    #     return (self.col, self.row).__hash__()

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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object : ({self.col}, {self.row})>"

    def normalize(self):
        return Vector(sign(self.col), sign(self.row))


class Position(Vector):
    def __init__(self, *args) -> None:
        try:
            if len(args) == 2:
                col,row = args
            elif len(args) == 1:
                col,row = args[0]
        except:
            raise PositionError("Can't initialize position. Try with string or integer arguments")
        if isinstance(col, str) and isinstance(row, str):
            try:
                col = ascii_lowercase[0:8].index(str(col))
                if isinstance(row, str):
                    row = int(row) - 1
            except:
                raise PositionError(f"Can't initialize position with arguments {col}, {row}. Try with a letter between a-h and a number between 1-8, for example 'e4'")
        if isinstance(col, int) and isinstance(row, int):
            if 0 <= min(row,col) and max(row,col) <= 7:
                self.col = col
                self.row = row
            else:
                raise PositionError(f"Row and col must be between 0 and 7")
        else:
            raise PositionError("Can't initialize position. Try with string or integer arguments")

    def __str__(self):
        return ascii_lowercase[0:8][self.col] + str(self.row + 1)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Position(self.col + other.col, self.row + other.row)
        else:
            raise TypeError(f"Can't add a Position to a {other.__class__}")

    def __hash__(self):
        return sixtyfour_primes[self.row*8 + self.col]
