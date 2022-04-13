from src.config.constants import INVALID_SQ
from src.core.classes.color import Color
from src.core.classes.ply import Ply
from src.core.error_classes.errors import PositionError


class TerminalPlayer:
    color: Color
    
    def __init__(self, color: Color) -> None:
        self.color = color

    def input_ply(self) -> Ply:
        while True:
            try:
                from_position = self.position(input(f"{str(self.color)} moves. Select starting square: "))
            except PositionError:
                print(INVALID_SQ)
            except Exception as err:
                raise err
            else:
                break
            # else:
            #     piece = board.get_piece(from_position)
            #     if piece:
            #         if piece.color == color:
            #             break
            #         else:
            #             print(INVALID_COLOR_MSG)
            #     else:
            #         print(EMPTY_SQ_MSG)
        while True:
            try:
                to_position = self.position(input("Select final square: "))
            except PositionError:
                print(INVALID_SQ)
            except Exception as err:
                raise err
            else:
                break

        return Ply(self.color, from_position, to_position)

    def input_promotion(self) -> type:
        while True:
            promotion_input = self.piece_class(input("Choose a piece to promote to: "))
            if promotion_input in [Queen, Knight, Bishop, Rook]:
                return promotion_input
            else:
                print(INVALID_PROMOTION)