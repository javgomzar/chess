from typing import Optional
from src.config.constants import IMG_DICT, UNICODE_DICT, BLACK,  WHITE
from src.core.classes.color import Black, Color, White
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
        try:
            __IPYTHON__
        except NameError:
            return self.unicode + ' '
        except Exception as err:
            raise err
        else:
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

class Knight(Piece):
    move_vectors = [Vector(sign_row*row, sign_col*col) for sign_row in [1,-1] for sign_col in [1,-1] for row,col in [(1,2),(2,1)]]
    image_file = "Knight.png"
    unicode = {
        Black(): '\u265E',
        White(): '\u2658'
    }

    def can_move(self, to_position: Position) -> bool:
        delta = abs(to_position - self.position)
        return delta.col * delta.row == 2

bishop_directions = [Vector(x,y) for x in [1,-1] for y in [1,-1]]

class Bishop(Piece):
    move_directions = bishop_directions
    move_vectors = [step*direction for step in range(1,8) for direction in bishop_directions]
    image_file = "Bishop.png"
    unicode = {
        Black(): '\u265D',
        White(): '\u2657'
    }

    def can_move(self, to_position: Position) -> bool:
        delta = abs(to_position - self.position)
        return delta.col == delta.row and delta.col != 0

rook_directions = [Vector(sign*vertical,sign*(1 - vertical)) for vertical in [0,1] for sign in [-1,1]]

class Rook(Piece):
    move_directions = rook_directions
    move_vectors = [step*direction for step in range(1,8) for direction in \
                   [Vector(sign*vertical,sign*(1 - vertical)) for vertical in [0,1] for sign in [-1,1]]]
    image_file = "Rook.png"
    unicode = {
        Black(): '\u265C',
        White(): '\u2656'
    }

    def can_move(self, to_position: Position) -> bool:
        delta = abs(to_position - self.position)
        return delta.col * delta.row == 0 and delta.col + delta.row != 0

class Queen(Piece):
    move_directions = bishop_directions + rook_directions
    move_vectors = [step*vector for step in range(1,8) for vector in bishop_directions + rook_directions]
    image_file = "Queen.png"
    unicode = {
        Black(): '\u265B',
        White(): '\u2655'
    }

    def can_move(self, to_position: Position) -> bool:
        delta = abs(to_position - self.position)
        return delta.col * delta.row * (delta.col - delta.row) == 0 and delta.col + delta.row != 0

class King(Piece):
    move_vectors = [Vector(x,y) for x in [-1,0,1] for y in [-1,0,1] if x != 0 or y != 0]
    image_file = "King.png"
    unicode = {
        Black(): '\u265A',
        White(): '\u2654'
    }

    def can_move(self, to_position: Position) -> bool:
        delta = abs(to_position - self.position)
        return max(delta.col, delta.row) == 1 and delta.col + delta.row != 0

    def is_left_castle(self, to_position: Position) -> bool:
        return not self.has_moved and (to_position - self.position) == Vector(-2,0)

    def is_right_castle(self, to_position: Position) -> bool:
        return not self.has_moved and (to_position - self.position) == Vector(2,0)

class Pawn(Piece):
    image_file = "Pawn.png"
    unicode = {
        Black(): '\u265F',
        White(): '\u2659'
    }

    def __init__(self, color: Color, position : Position = None, is_active : bool = False, has_moved : bool = False) -> None:
        super().__init__(color, position, is_active, has_moved)
        self.move_vectors = [step*color.pawn_direction for step in [1,2]] + \
                               [Vector(delta_col, color.pawn_direction.row) for delta_col in [1,-1]]

    def can_move(self, to_position: Position) -> bool:
        delta = to_position - self.position
        return abs(delta.col) == 1 and delta.row == self.color.pawn_direction.row or \
               abs(delta.col) == 0 and (delta.row == self.color.pawn_direction.row or
               not self.has_moved and delta.row == 2*self.color.pawn_direction.row)

    def is_capture(self, to_position: Position):
        delta = to_position - self.position
        return abs(delta.col) == 1 and delta.row == self.color.pawn_direction.row
