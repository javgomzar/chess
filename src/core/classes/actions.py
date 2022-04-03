from dataclasses import dataclass, field
from src.core.classes.color import Black, White
from src.core.error_classes.errors import AddError
from src.core.classes.action import Action
from src.core.classes.piece import Bishop, King, Knight, Pawn, Queen, Rook
from src.core.classes.position import Position
from src.core.classes.board import Board
from src.core.classes.board import Piece

# @dataclass
# class Add():
#     piece : Piece
#     position : Position

#     def execute(self, board : Board) -> None:
#         if self.piece in board.pieces:
#             raise AddError(f"Can't add the {self.piece.__class__.__name__.lower()} to a board that alredy contains the piece.")
#         elif board.get_piece(self.position):
#             raise AddError(f"Can't add the {self.piece.__class__.__name__.lower()} to {self.position} that is alredy occupied.")
#         else:
#             self.piece.position = self.position
#             self.piece.is_active = True
#             board.pieces.append(self.piece)

#     def undo(self, board : Board) -> None:
#         board.pieces.remove(self.piece)

#     def redo(self, board : Board) -> None:
#         self.piece.position = self.position
#         self.piece.is_active = True
#         board.pieces.append(self.piece)

@dataclass
class Remove():
    piece : Piece

    def execute(self, board : Board) -> None:
        if not self.piece:
            return
        if not self.piece in board.pieces:
            raise Exception()
        if not self.piece.is_active:
            raise Exception()
        self.piece.is_active = False

    def undo(self, board : Board) -> None:
        self.piece.is_active = True

    def redo(self, board : Board) -> None:
        self.piece.is_active = False

@dataclass
class FirstMove():
    piece : Piece
    to_position : Position

    def execute(self, board : Board) -> None:
        self.from_position = self.piece.position
        if not self.piece in board.pieces:
            raise Exception()
        elif not self.piece.is_active:
            raise Exception()
        elif board.get_piece(self.to_position):
            raise Exception()
        elif self.piece.has_moved:
            raise Exception()
        else:
            self.piece.position = self.to_position
            self.piece.has_moved = True

    def undo(self, board : Board) -> None:
        self.piece.position = self.from_position
        self.piece.has_moved = False

    def redo(self, board : Board) -> None:
        self.piece.position = self.to_position
        self.piece.has_moved = True

@dataclass
class Move():
    piece : Piece
    to_position : Position

    def execute(self, board : Board) -> None:
        self.from_position = self.piece.position
        if not self.piece in board.pieces:
            raise Exception()
        elif not self.piece.is_active:
            raise Exception()
        elif board.get_piece(self.to_position):
            raise Exception()
        elif not self.piece.has_moved:
            raise Exception()
        else:
            self.piece.position = self.to_position

    def undo(self, board : Board) -> None:
        self.piece.position = self.from_position

    def redo(self, board : Board) -> None:
        self.piece.position = self.to_position


@dataclass
class Promote():
    piece : Pawn
    to_piece : Piece

    def execute(self, board : Board) -> None:
        board.pieces.remove(self.piece)
        self.to_piece.position = self.piece.position
        board.pieces.append(self.to_piece)

    def undo(self, board : Board) -> None:
        board.pieces.remove(self.to_piece)
        board.pieces.append(self.piece)

    def redo(self, board : Board) -> None:
        board.pieces.remove(self.piece)
        board.pieces.append(self.piece)

class EnPassant():
    piece: Pawn
    to_position: Position

    def execute(self, board: Board) -> None:
        self.from_position = self.piece.position
        taken_pawn = board.get_piece(self.to_position + (-self.piece.color.pawn_direction))
        taken_pawn.is_active = False


@dataclass
class Batch():
    commands : list[Action]

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

# @dataclass
# class InitStdBoard(Batch):
#     commands : list[Action] = field(default_factory=lambda:
#         [Add(piece_class(color), Position(col,row)) \
#             for color in [Black(), White()] 
#             for col,class_pair in enumerate(zip([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook],[Pawn]*8))
#             for row,piece_class in zip((color.king_row_index, color.pawn_row_index),class_pair)])
