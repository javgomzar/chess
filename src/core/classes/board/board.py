from ..pieces import Knight
from ..actions import ActionController
from ..position import Position


class Board(ActionController):
    """
    Class for a chess board. Initializes being empty.
    """

    def __str__(self) -> str:
        """
        Returns a string with a simple representation of the state of the board.
        """
        hash = ''
        for row in reversed(range(0,8)):
            for col in range(0,8):
                piece = self.get_piece(Position(col,row))
                if piece:
                    piece_hash = 'N' if isinstance(piece, Knight) else piece.__class__.__name__[0]
                    color_hash = piece.color.__class__.__name__[0]
                    hash += color_hash + piece_hash
                else:
                    hash += '  '
                hash += '-'
            hash += '\n'
        return hash

    def copy(self):
        """
        Returns a copy with the same pieces and same undo history. Redo history is cleared.
        """
        new_instance = self.__class__()
        for piece in self:
            new_instance.add(piece.copy(), self.get_position(piece))
        new_instance.undo_stack = self.undo_stack
        return new_instance
