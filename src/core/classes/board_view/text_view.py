from ..board import Board
from src.config.constants import EMPTY_BOARD_STRING
from .board_view import BoardView
from ..color import *
from ..pieces import *


class TextView(BoardView):
    unicode_dict: dict = {
        Black(): {
            King: "\u265A",
            Queen: "\u265B",
            Rook: "\u265C",
            Bishop: "\u265D",
            Knight: "\u265E",
            Pawn: "\u265F"
        },
        White(): {
            King: "\u2654", 
            Queen: "\u2655",
            Rook: "\u2656",
            Bishop: "\u2657",
            Knight: "\u2658",
            Pawn: "\u2659"
        }
    }

    def show_board(self, board: Board) -> None:
        result = EMPTY_BOARD_STRING
        for row in range(0,8):
            for col in range(0,8):
                piece = board.get_piece(Position(col,row))
                if piece:
                    symbol = self.unicode_dict[piece.color][piece.__class__]
                    if not hasattr(__builtins__, '__IPYTHON__'):
                        symbol += " "
                else:
                    symbol = "  "
                result = result.replace(str(row+1) + str(col+1), symbol)
        print(result)

    def alert_check(self) -> None:
        print("Check!")

    def win(self, color: Color) -> None:
        print(f"Check mate. {color} wins!")

    def lose(self, color: Color) -> None:
        print(f"Check mate. {color} lost.")

    def draw(self) -> None:
        print("It's a draw.")

    def invalid_move(self) -> None:
        print("Invalid move.")
