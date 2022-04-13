from dataclasses import dataclass
from src.core.classes.board import Board
from src.core.classes.color import Color
from src.core.classes.position import Position, Vector


@dataclass
class Castle:
    color: Color
    direction: Vector

    def execute(self, board: Board) -> None:
        king_position = Position(4, self.color.king_row)
        self.rook_col = 7 if self.direction.col > 0 else 0
        self.final_king_col,self.final_rook_col = (6,5) if self.direction.col > 0 else (2,3)
        self.king = board.get_piece(king_position)
        self.rook = board.get_piece(Position(self.rook_col, self.color.king_row))

        board.set_position(self.king, Position(self.final_king_col, self.color.king_row))
        board.set_position(self.rook, Position(self.final_rook_col, self.color.king_row))
        self.rook.has_moved = True
        self.king.has_moved = True

    def undo(self, board: Board) -> None:
        board.set_position(self.king, Position(4, self.color.king_row))
        board.set_position(self.rook, Position(self.rook_col, self.color.king_row))
        self.rook.has_moved = False
        self.king.has_moved = False

    def redo(self, board: Board) -> None:
        board.set_position(self.king, Position(self.final_king_col, self.color.king_row))
        board.set_position(self.rook, Position(self.final_rook_col, self.color.king_row))
        self.rook.has_moved = False
        self.king.has_moved = False 
