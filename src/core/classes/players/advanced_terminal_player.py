from ..pieces import piece_class_from_text
from ..error_classes import InvalidInput
from ..board import Board
from .terminal_player import TerminalPlayer
from ..error_classes import AmbiguousMove
from ..ply import Ply, ply_from_notation


class AdvancedTerminalPlayer(TerminalPlayer):
    def input_promotion(self, board: Board) -> type:
        return self.to_piece_class

    def input_ply(self, board: Board) -> Ply:
        while True:
            try:
                notation = input(f"{str(self.color)} moves. Select move in algebraic notation: ")
                ply = ply_from_notation(self.color, notation, board)
                if notation[-1] in ["B","P","Q","R"]:
                    self.to_piece_class = piece_class_from_text(notation[-1])
            except AmbiguousMove:
                print("Ambiguous move.")
            except InvalidInput:
                print("Invalid input.")
            except Exception as err:
                raise err
            else:
                break
        return ply
