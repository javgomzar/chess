from ..pieces import Knight
from ..actions import ActionController
from src.config.constants import BOARD_IMG, EMPTY_BOARD_STRING
from PIL import Image
from ..position import Position


class Board(ActionController):
    """
    Class for a chess board. If no arguments are given to the constructor,
    the board will start as the standard chess initial board.
    """

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

    def string_hash(self) -> str:
        hash = ''
        for row in range(0,8):
            for col in range(0,8):
                piece = self.get_piece(Position(col,row))
                if piece:
                    piece_hash = 'N' if isinstance(piece, Knight) else piece.__class__.__name__[0]
                    color_hash = piece.color.__class__.__name__[0]
                    hash += color_hash + piece_hash
                hash += '-'
        return hash

    def image(self) -> Image:
        board_img = Image.open(BOARD_IMG)

        for piece in self.get_pieces(is_active=True):
            piece_img = piece.image()
            position = self.get_position(piece)
            board_img.paste(piece_img, (50*(position.col - 1), 50*(8 - position.row)), piece_img)
        
        return board_img
