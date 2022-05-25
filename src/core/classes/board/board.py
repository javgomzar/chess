from ..pieces import Knight
from ..actions import ActionController
from ..position import Position


class Board(ActionController):
    """
    Class for a chess board. If no arguments are given to the constructor,
    the board will start as the standard chess initial board.
    """

    def string_hash(self) -> str:
        """
        Returns a string with a representation of the state of the board.
        """
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
