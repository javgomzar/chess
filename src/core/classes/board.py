from dataclasses import dataclass, field
from typing import Optional
from collections.abc import MutableMapping
from src.config.constants import BLACK, BOARD_IMG, WHITE, LEFT, RIGHT, EMPTY_BOARD_STRING, EMPTY_SQ_MSG
from src.core.classes.color import Black, Color, White
from src.core.classes.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from PIL import Image
from src.core.classes.position import Position


class Board():
    """
    Class for a chess board. If no arguments are given to the constructor,
    the board will start as the standard chess initial board.
    """
    pieces : list[Piece]

    def __init__(self, empty : bool = False):
        if not empty:
            self.pieces = [piece_class(color,Position(col,row),is_active=True,has_moved=False)
                            for color in [Black(), White()] 
                            for col,class_pair in enumerate(zip([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook],[Pawn]*8))
                            for row,piece_class in zip((color.king_row, color.pawn_row),class_pair)]
        else:
            self.pieces = []

    def __str__(self) -> str:
        result = EMPTY_BOARD_STRING
        for row in range(0,8):
            for col in range(0,8):
                piece = self.get_piece(Position(col,row))
                if piece and piece.is_active:
                    symbol = str(piece)
                else:
                    symbol = "  "
                result = result.replace(str(row+1) + str(col+1), symbol)
        return result

    def __contains__(self, piece: Piece) -> bool:
        for try_piece in self.pieces:
            if piece == try_piece:
                return True
        else:
            return False

    def __eq__(self, other) -> bool:
        if len(self.pieces) == len(other.pieces):
            for piece in self.pieces:
                if piece not in other.pieces:
                    return False
            return True
        return False

    def image(self) -> Image:
        board_img = Image.open(BOARD_IMG)

        for piece in [piece for piece in self.pieces if piece.is_active]:
            piece_img = piece.image()
            board_img.paste(piece_img, (50*(piece.position[1] - 1), 50*(8 - piece.position[0])), piece_img)
        
        return board_img

    def get_piece(self, position : Position) -> Optional[Piece]:
        pieces = [piece for piece in self.pieces if piece.position == position and piece.is_active]
        if len(pieces) == 0:
            return None
        elif len(pieces) > 1:
            raise Exception()
        else:
            return pieces[0]

    def get_pieces(self, color : Optional[Color] = None, is_active : Optional[bool] = None) -> list[Piece]:
        pieces = self.pieces
        if color:
            pieces = [piece for piece in pieces if piece.color == color]
        if is_active != None:
            pieces = [piece for piece in pieces if piece.is_active == is_active]
        return pieces

    def get_king(self, color: Color) -> King:
        pieces = [piece for piece in self.pieces if isinstance(piece, King) and piece.color == color]
        if len(pieces) == 0:
            return None
        elif len(pieces) > 1:
            raise Exception()
        else:
            return pieces[0]

    def copy(self):
        board = Board(empty=True)
        for piece in self.pieces:
            board.pieces.append(piece.copy())
        return board
