from dataclasses import dataclass
from src.core.classes.board import Board
from src.core.classes.position import Position
from src.core.classes.pieces import Pawn


@dataclass
class EnPassant:
    piece: Pawn
    to_position: Position

    def execute(self, board: Board) -> None:
        self.taken_position = self.to_position + (-self.piece.color.pawn_direction)
        self.taken_pawn = board.get_piece(self.taken_position)
        self.from_position = board.get_position(self.piece)
        board.set_position(self.piece, self.to_position)
        board.remove(self.taken_pawn)

    def undo(self, board: Board) -> None:
        board.set_position(self.piece, self.from_position)
        board.set_position(self.taken_pawn, self.taken_position)

    def redo(self, board: Board) -> None:
        board.set_position(self.piece, self.to_position)
        board.remove(self.taken_pawn)
