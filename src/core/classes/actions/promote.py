from dataclasses import dataclass, field

from ..pieces import PieceManager
from ..vector import Vector
from ..pieces import Pawn

from .move import Move


@dataclass
class Promote:
    piece : Pawn
    vector : Vector
    is_filled : bool = field(default=False, init=False)

    def process(self, piece_manager : PieceManager) -> None:
        self.from_position = piece_manager.get_position(self.piece)
        self.to_position = self.from_position + self.vector
        self.move = Move(self.piece, self.vector)

    def execute(self, piece_manager : PieceManager) -> None:
        self.move.execute(piece_manager)
        if self.is_filled:
            self.to_piece = self.to_piece_class(self.piece.color, has_moved=True)
            piece_manager.replace(self.piece, self.to_piece)

    def undo(self, piece_manager : PieceManager) -> None:
        if self.is_filled:
            piece_manager.replace(self.to_piece, self.piece)
        self.move.undo(piece_manager)

    def redo(self, piece_manager : PieceManager) -> None:
        self.move.redo(piece_manager)
        if self.is_filled:
            piece_manager.replace(self.piece, self.to_piece)
