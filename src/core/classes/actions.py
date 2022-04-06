from dataclasses import dataclass
from src.core.classes.color import Color
from src.core.classes.input import Input
from src.core.classes.action import Action
from src.core.classes.piece import Pawn, Piece
from src.core.classes.position import Position
from src.core.classes.board import Board

@dataclass(eq=True)
class Move():
    piece : Piece
    to_position : Position

    def execute(self, board : Board) -> None:
        if self.piece not in board.pieces:
            raise Exception()
        elif not self.piece.is_active:
            raise Exception()
        else:
            self.taken_piece = board.get_piece(self.to_position)
            self.from_position = self.piece.position
            self.is_first = not self.piece.has_moved

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
        if self.piece.position.row != self.piece.color.opposite_color().king_row:
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
        self.taken_pawn = board.get_piece(self.to_position + (-self.piece.color.pawn_direction))
        self.from_position = self.piece.position
        self.piece.position = self.to_position
        self.taken_pawn.is_active = False

    def undo(self, board: Board) -> None:
        self.piece.position = self.from_position
        self.taken_pawn.is_active = True

    def redo(self, board: Board) -> None:
        self.from_position = self.piece.position
        self.taken_pawn.is_active = False

@dataclass(eq=True)
class LeftCastle():
    color : Color

    def execute(self, board : Board) -> None:
        self.king = board.get_king(self.color)
        self.rook = board.get_piece(Position(0,self.color.king_row))
        self.king.position = Position(2, self.color.king_row)
        self.rook.position = Position(3, self.color.king_row)

    def undo(self, board : Board) -> None:
        self.king.position = Position(4, self.color.king_row)
        self.rook.position = Position(0, self.color.king_row)

    def redo(self, board : Board) -> None:
        self.king.position = Position(2, self.color.king_row)
        self.rook.position = Position(3, self.color.king_row)

@dataclass(eq=True)
class RightCastle():
    color : Color

    def execute(self, board : Board) -> None:
        self.king = board.get_king(self.color)
        self.rook = board.get_piece(Position(0,self.color.king_row))
        self.king.position = Position(6, self.color.king_row)
        self.rook.position = Position(5, self.color.king_row)

    def undo(self, board : Board) -> None:
        self.king.position = Position(4, self.color.king_row)
        self.rook.position = Position(7, self.color.king_row)

    def redo(self, board : Board) -> None:
        self.king.position = Position(6, self.color.king_row)
        self.rook.position = Position(5, self.color.king_row)