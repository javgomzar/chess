from dataclasses import dataclass
from ..pieces import PieceManager
from src.core.classes.position import Vector
from ..pieces import Piece


@dataclass
class Move:
    piece : Piece
    vector : Vector

    def process(self, piece_manager : PieceManager) -> None:
        self.from_position = piece_manager.get_position(self.piece)
        self.to_position = self.from_position + self.vector
        self.taken_piece = piece_manager.get_piece(self.to_position)
        self.is_first = not self.piece.has_moved

    def execute(self, piece_manager : PieceManager) -> None:
        if self.taken_piece:
            piece_manager.remove(self.taken_piece)
        piece_manager.set_position(self.piece, self.to_position)
        self.piece.has_moved = True

    def undo(self, piece_manager : PieceManager) -> None:
        piece_manager.set_position(self.piece, self.from_position)
        if self.is_first:
            self.piece.has_moved = False
        if self.taken_piece:
            piece_manager.set_position(self.taken_piece, self.to_position)

    def redo(self, piece_manager : PieceManager) -> None:
        if self.taken_piece:
            piece_manager.remove(self.taken_piece)
        piece_manager.set_position(self.piece, self.to_position)
        self.piece.has_moved = True
