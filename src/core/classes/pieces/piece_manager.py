from ..color import Color
from . import Piece, King
from ..position import Position
from src.utils import extract


class PieceManager:
    """
    """
    piece_positions : dict[Piece, Position]
    _last_id : int

    def __init__(self, pieces: list[tuple[Piece,Position]]=[]) -> None:
        self._last_id = 0
        self.piece_positions = {}

        for piece,position in pieces:
            self.add(piece, position)

    def __contains__(self, piece: Piece) -> bool:
        for try_piece in self:
            if piece is try_piece:
                return True
        else:
            return False

    def __iter__(self):
        return iter(self.piece_positions.keys())

    def _set_id(self, piece: Piece) -> None:
        piece.id = self._last_id
        self._last_id += 1

    def get_position(self, piece: Piece) -> Position:
        return self.piece_positions[piece]

    def set_position(self, piece: Piece, position: Position) -> None:
        if self.get_piece(position):
            raise Exception("There is alredy a piece in that position.")
        elif not position:
            raise Exception("To set position of piece to None use method remove()")
        self.piece_positions[piece] = position

    def add(self, piece: Piece, position: Position) -> None:
        self._set_id(piece)
        self.piece_positions[piece] = position

    def remove(self, piece: Piece) -> None:
        self.piece_positions[piece] = None

    def delete(self, piece: Piece) -> None:
        del self.piece_positions[piece]

    def replace(self, old_piece: Piece, new_piece: Piece) -> None:
        position = self.get_position(old_piece)
        self.delete(old_piece)
        new_piece.id = old_piece.id
        self.set_position(new_piece, position)

    def get_piece(self, position : Position) -> Piece:
        if not position:
            raise Exception("Position argument must be provided.")
        return extract([piece for piece in self if self.get_position(piece) == position])

    def get_king_position(self, color: Color) -> Position:
        return extract([self.get_position(piece) for piece in self.get_pieces(color) if isinstance(piece, King)])

    def get_pieces(self, color : Color = None, is_active : bool = None, piece_type: type = None, exclude_type: type = None) -> list[Piece]:
        pieces = self.__iter__()
        if color:
            pieces = [piece for piece in pieces if piece.color == color]
        if is_active != None:
            if is_active:
                pieces = [piece for piece in pieces if self.get_position(piece)]
            else:
                pieces = [piece for piece in pieces if not self.get_position(piece)]
        if piece_type:
            pieces = [piece for piece in pieces if isinstance(piece, piece_type)]
        if exclude_type:
            pieces = [piece for piece in pieces if not isinstance(piece, exclude_type)]

        return sorted(pieces, key=int)
