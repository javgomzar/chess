from dataclasses import dataclass
from ..pieces import PieceManager
from ..color import Color
from src.core.classes.position import Position, Vector


@dataclass
class Castle:
    color: Color
    direction: Vector

    def process(self, piece_manager: PieceManager) -> None:
        king_position = Position(4, self.color.king_row)
        self.rook_col = 7 if self.direction.col > 0 else 0
        self.final_king_col,self.final_rook_col = (6,5) if self.direction.col > 0 else (2,3)
        self.piece = piece_manager.get_piece(king_position)
        self.rook = piece_manager.get_piece(Position(self.rook_col, self.color.king_row))

    def execute(self, piece_manager: PieceManager) -> None:
        piece_manager.set_position(self.piece, Position(self.final_king_col, self.color.king_row))
        piece_manager.set_position(self.rook, Position(self.final_rook_col, self.color.king_row))
        self.rook.has_moved = True
        self.piece.has_moved = True

    def undo(self, piece_manager: PieceManager) -> None:
        piece_manager.set_position(self.piece, Position(4, self.color.king_row))
        piece_manager.set_position(self.rook, Position(self.rook_col, self.color.king_row))
        self.rook.has_moved = False
        self.piece.has_moved = False

    def redo(self, piece_manager: PieceManager) -> None:
        piece_manager.set_position(self.piece, Position(self.final_king_col, self.color.king_row))
        piece_manager.set_position(self.rook, Position(self.final_rook_col, self.color.king_row))
        self.rook.has_moved = False
        self.piece.has_moved = False 
