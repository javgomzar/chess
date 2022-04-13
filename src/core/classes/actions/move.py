from dataclasses import dataclass
from src.core.classes.board import Board
from src.core.classes.position import Vector
from core.classes.pieces.piece import Piece


@dataclass
class Move:
    piece : Piece
    vector : Vector

    def execute(self, board : Board) -> None:
        self.from_position = board.get_position(self.piece)
        self.to_position = self.from_position + self.vector
        self.taken_piece = board.get_piece(self.to_position)
        self.is_first = not self.piece.has_moved
        if self.taken_piece:
            board.remove(self.taken_piece)
        board.set_position(self.piece, self.to_position)
        self.piece.has_moved = True

    def undo(self, board : Board) -> None:
        board.set_position(self.piece, self.from_position)
        if self.is_first:
            self.piece.has_moved = False
        if self.taken_piece:
            board.set_position(self.taken_piece, self.to_position)

    def redo(self, board : Board) -> None:
        if self.taken_piece:
            board.remove(self.taken_piece)
        board.set_position(self.piece, self.to_position)
        self.piece.has_moved = True
        