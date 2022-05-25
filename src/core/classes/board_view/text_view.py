from ..board import Board
from .board_view import BoardView
from ..color import *
from ..pieces import *


EMPTY_BOARD_STRING = "  ╔════╤════╤════╤════╤════╤════╤════╤════╗\n" + \
                     "8 ║ 81 │ 82 │ 83 │ 84 │ 85 │ 86 │ 87 │ 88 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "7 ║ 71 │ 72 │ 73 │ 74 │ 75 │ 76 │ 77 │ 78 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "6 ║ 61 │ 62 │ 63 │ 64 │ 65 │ 66 │ 67 │ 68 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "5 ║ 51 │ 52 │ 53 │ 54 │ 55 │ 56 │ 57 │ 58 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "4 ║ 41 │ 42 │ 43 │ 44 │ 45 │ 46 │ 47 │ 48 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "3 ║ 31 │ 32 │ 33 │ 34 │ 35 │ 36 │ 37 │ 38 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "2 ║ 21 │ 22 │ 23 │ 24 │ 25 │ 26 │ 27 │ 28 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "1 ║ 11 │ 12 │ 13 │ 14 │ 15 │ 16 │ 17 │ 18 ║\n" + \
                     "  ╚════╧════╧════╧════╧════╧════╧════╧════╝\n" + \
                     "    a    b    c    d    e    f    g    h   "


class TextView(BoardView):
    """
    Board view for a console. The board will be rendered printing strings.
    Be aware that you should use a font that supports Unicode.
    """
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
                    # With IPython pieces characters occupy two spaces in a monospace font,
                    # but without it they will only take one space
                    if not hasattr(__builtins__, '__IPYTHON__'):
                        symbol += " "
                else:
                    symbol = "  "
                # We replace each number with the corresponding square.
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
