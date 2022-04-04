from dataclasses import dataclass, field
from typing import Optional
from src.core.classes.input import Input
from src.core.classes.action import Action
from src.core.classes.piece import Bishop, Knight, Pawn, Queen, Rook
from src.core.classes.position import Position
from src.core.classes.board import Board
from src.core.classes.board import Piece

@dataclass(eq=True)
class Move():
    piece : Piece
    to_position : Position

    def execute(self, board : Board) -> None:
        self.taken_piece = board.get_piece(self.to_position)
        self.from_position = self.piece.position
        self.is_first = not self.piece.has_moved

        if self.piece not in board.pieces:
            raise Exception()
        elif not self.piece.is_active:
            raise Exception()
        elif board.get_piece(self.to_position):
            raise Exception()
        elif self.piece.has_moved:
            raise Exception()
        else:
            if self.taken_piece:
                self.taken_piece.is_active = False
            self.piece.position = self.to_position
            self.piece.has_moved = True

    def undo(self, board : Board) -> None:
        self.piece.position = self.from_position
        if self.is_first:
            self.piece.has_moved = False
        if self.taken_piece:
            self.taken_piece.is_active = True

    def redo(self, board : Board) -> None:
        self.piece.position = self.to_position
        self.piece.has_moved = True
        if self.taken_piece:
            self.taken_piece.is_active = False

@dataclass(eq=True)
class Batch():
    commands : list[Action]

    def __len__(self):
        return len(self.commands)

    def __contains__(self, action: Action) -> bool:
        for command in self.commands:
            if command == action:
                return True
        else:
            return True

    def execute(self, board : Board):
        completed_commands = []
        try:
            for action in self.commands:
                action.execute(board)
                completed_commands.append(action)
        except Exception as err:
            for action in reversed(completed_commands):
                action.undo(board)
            raise err

    def undo(self, board : Board) -> None:
        for action in self.commands:
            action.undo(board)

    def redo(self, board : Board) -> None:
        for action in self.commands:
            action.redo(board)

@dataclass(eq=True)
class Promote():
    piece : Pawn

    def execute(self, board : Board) -> None:
        if self.piece.position.row != self.piece.color.opposite_color().king_row_index:
            raise Exception()
        piece_class = Input.promotion()
        self.to_piece = piece_class(color=self.piece.color, piece=self.piece.position, is_active=True, has_moved = True)
        board.pieces.remove(self.piece)
        board.pieces.append(self.to_piece)

    def undo(self, board : Board) -> None:
        board.pieces.remove(self.to_piece)
        board.pieces.append(self.piece)

    def redo(self, board : Board) -> None:
        board.pieces.remove(self.piece)
        board.pieces.append(self.piece)

@dataclass(eq=True)
class EnPassant():
    piece: Pawn
    to_position: Position

    def execute(self, board: Board) -> None:
        self.from_position = self.piece.position
        taken_pawn = board.get_piece(self.to_position + (-self.piece.color.pawn_direction))
        taken_pawn.is_active = False