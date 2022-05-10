from ..pieces import Bishop, King, Knight, Pawn, Queen, Rook
from ..board import Board
from ..position import Position
from src.config.constants import BISHOP_NAMES, INVALID_MOVE_MSG, INVALID_PROMOTION, INVALID_SQ, KING_NAMES, KNIGHT_NAMES, PAWN_NAMES, QUEEN_NAMES, TOWER_NAMES
from ..color import Color
from ..ply import Ply
from ..error_classes import PositionError


class TerminalPlayer:
    color: Color

    def __init__(self, color: Color):
        self.color = color

    def show_board(self, board: Board) -> None:
        print(board)

    def invalid_move(self) -> None:
        print(INVALID_MOVE_MSG)

    def alert_check(self) -> None:
        print("Check!")

    def win(self) -> None:
        print(f"Check mate. {self.color} wins!")

    def lose(self) -> None:
        print("Check mate. You lost.")

    def draw(self) -> None:
        print("It's a draw.")

    def input_ply(self, board: Board) -> Ply:
        while True:
            try:
                from_position = Position.from_notation(input(f"{str(self.color)} moves. Select starting square: "))
            except PositionError:
                print(INVALID_SQ)
            except Exception as err:
                raise err
            else:
                break
        while True:
            try:
                to_position = Position.from_notation(input("Select final square: "))
            except PositionError:
                print(INVALID_SQ)
            except Exception as err:
                raise err
            else:
                break

        return Ply(self.color, from_position, to_position)

    def input_promotion(self, board: Board) -> type:
        while True:
            x = input("Choose a piece to promote to: ")
            print(x)
            promotion_input = self.input_piece_class(x)
            if promotion_input in [Queen, Knight, Bishop, Rook]:
                return promotion_input
            else:
                print(INVALID_PROMOTION)

    def input_piece_class(self, name: str) -> type:
        """
        This function standardizes the chess piece names.
        """
        if name in PAWN_NAMES:
            return Pawn
        elif name in KNIGHT_NAMES:
            return Knight
        elif name in BISHOP_NAMES:
            return Bishop
        elif name in TOWER_NAMES:
            return Rook
        elif name in QUEEN_NAMES:
            return Queen
        elif name in KING_NAMES:
            return King
        else:
            return None
