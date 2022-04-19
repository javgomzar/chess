from src.config.constants import BOARD_IMG, EMPTY_BOARD_STRING
from src.core.classes.color import Color
from src.core.classes.pieces.piece import Piece
from src.core.classes.pieces import King
from PIL import Image
from src.core.classes.position import Position
from src.utils import extract


class Board():
    """
    Class for a chess board. If no arguments are given to the constructor,
    the board will start as the standard chess initial board.
    """
    positions : dict[Piece, Position]

    def __init__(self) -> None:
        self._last_id = 0
        self.positions = {}

    def __str__(self) -> str:
        result = EMPTY_BOARD_STRING
        for row in range(0,8):
            for col in range(0,8):
                piece = self.get_piece(Position(col,row))
                if piece:
                    symbol = str(piece)
                else:
                    symbol = "  "
                result = result.replace(str(row+1) + str(col+1), symbol)
        return result

    def __contains__(self, piece: Piece) -> bool:
        for try_piece in self:
            if piece is try_piece:
                return True
        else:
            return False

    def __iter__(self):
        return iter(self.positions.keys())

    def __hash__(self):
        result = 1
        for piece in self:
            position = self.positions[piece]
            if position:
                result *= position.__hash__() ** int(piece)
        return result

    def _set_id(self, piece: Piece) -> None:
        piece.id = self._last_id
        self._last_id += 1

    # def __eq__(self, other) -> bool:
    #     try:
    #         other.positions
    #     except:
    #         return False
    #     if isinstance(other.positions, dict) and len(self.positions) == len(other.positions):
    #         for piece in self.positions.keys():
    #             if piece not in other.positions.keys():
    #                 break
    #         else:
    #             return True
    #     return False

    def image(self) -> Image:
        board_img = Image.open(BOARD_IMG)

        for piece in self.get_pieces(is_active=True):
            piece_img = piece.image()
            position = self.get_position(piece)
            board_img.paste(piece_img, (50*(position.col - 1), 50*(8 - position.row)), piece_img)
        
        return board_img

    def get_position(self, piece: Piece) -> Position:
        return self.positions[piece]

    def set_position(self, piece: Piece, position: Position) -> None:
        # if piece.__class__ == King:
        #     raise Exception()
        if self.get_piece(position):
            raise Exception("There is alredy a piece in that position.")
        elif not position:
            raise Exception("To set position of piece to none use method remove()")
        self.positions[piece] = position

    def add(self, piece: Piece, position: Position) -> None:
        self._set_id(piece)
        self.positions[piece] = position

    def remove(self, piece: Piece) -> None:
        self.positions[piece] = None

    def delete(self, piece: Piece) -> None:
        del self.positions[piece]

    def replace(self, piece: Piece, with_piece: Piece) -> None:
        position = self.get_position(piece)
        self.delete(piece)
        self.set_position(with_piece, position)

    def get_piece(self, position : Position) -> Piece:
        if not position:
            raise Exception("Position argument must be provided.")
        return extract([piece for piece in self.positions.keys() if self.get_position(piece) == position])

    def get_king_position(self, color: Color) -> Position:
        return extract([self.get_position(piece) for piece in self.get_pieces(color) if isinstance(piece, King)])

    def get_pieces(self, color : Color = None, is_active : bool = None) -> list[Piece]:
        pieces = self.__iter__()
        if color:
            pieces = [piece for piece in pieces if piece.color == color]
        if is_active != None:
            if is_active:
                pieces = [piece for piece in pieces if self.get_position(piece)]
            else:
                pieces = [piece for piece in pieces if not self.get_position(piece)]
        return pieces

    def copy(self):
        board = Board()
        for piece in self:
            board.add(piece.copy(), self.get_position(piece))
        return board
