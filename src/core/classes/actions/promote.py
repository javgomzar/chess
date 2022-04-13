from dataclasses import dataclass, field
from src.core.classes.actions.move import Move
from src.core.classes.board import Board
from src.core.classes.position import Vector
from src.core.classes.pieces import Pawn


@dataclass
class Promote:
    piece : Pawn
    vector : Vector
    is_filled : bool = field(default=False, init=False)

    def execute(self, board : Board) -> None:
        self.from_position = board.get_position(self.piece)
        self.to_position = self.from_position + self.vector
        self.move = Move(self.piece, self.vector)
        self.move.execute(board)
        if self.is_filled:
            self.to_piece = self.to_piece_class(self.piece.color, has_moved=True)
            board.replace(self.piece, self.to_piece)

    def undo(self, board : Board) -> None:
        if self.is_filled:
            board.replace(self.to_piece, self.piece)
        self.move.undo(board)

    def redo(self, board : Board) -> None:
        self.move.redo(board)
        if self.is_filled:
            board.replace(self.piece, self.to_piece)

    # def choose(self) -> None:
    #     self.to_piece_class = Input.promotion()
    #     self.is_filled = True
