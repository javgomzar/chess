from src.config.constants import INVALID_PROMOTION, INVALID_SQ

from ..pieces import Bishop, Knight, Queen, Rook, piece_class_from_text
from ..board import Board
from ..position import Position
from ..ply import Ply
from ..error_classes import PositionError

from .player import Player


class TerminalPlayer(Player):
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
            promotion_input = piece_class_from_text(x)
            if promotion_input in [Queen, Knight, Bishop, Rook]:
                return promotion_input
            else:
                print(INVALID_PROMOTION)

