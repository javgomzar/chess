
from string import ascii_lowercase
from .error_classes.errors import PositionError
from .vector import Vector


class Position(Vector):
    def __init__(self, col: int, row: int):
        if 0 <= min(row,col) and max(row,col) <= 7:
                self.col = col
                self.row = row
        else:
            raise PositionError(f"Row and col must be between 0 and 7")

    def __repr__(self):
        return f"<{self.__class__.__name__} object : ({self.col}, {self.row}), '{self.__str__()}'>"

    def __str__(self) -> str:
        return ascii_lowercase[0:8][self.col] + str(self.row + 1)

    def __hash__(self) -> int:
        return 8*self.col + self.row

    def __int__(self):
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
