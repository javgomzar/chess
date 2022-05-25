from dataclasses import dataclass
from ..pieces import PieceManager
from src.core.classes.position import Position
from ..pieces import Pawn


@dataclass
class EnPassant:
    piece: Pawn
    to_position: Position

    def process(self, piece_manager: PieceManager) -> None:
        self.taken_position = self.to_position + (-self.piece.color.pawn_direction)
        self.taken_pawn = piece_manager.get_piece(self.taken_position)
        self.from_position = piece_manager.get_position(self.piece)

    def execute(self, piece_manager: PieceManager) -> None:
        piece_manager.set_position(self.piece, self.to_position)
        piece_manager.remove(self.taken_pawn)

    def undo(self, piece_manager: PieceManager) -> None:
        piece_manager.set_position(self.piece, self.from_position)
        piece_manager.set_position(self.taken_pawn, self.taken_position)

    def redo(self, piece_manager: PieceManager) -> None:
        piece_manager.set_position(self.piece, self.to_position)
        piece_manager.remove(self.taken_pawn)
