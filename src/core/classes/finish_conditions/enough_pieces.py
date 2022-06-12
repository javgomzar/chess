from .finish_condition import FinishCondition
from .final_states import FinalState, Draw
from ..ply import Ply
from ..board import Board
from ..color import *
from ..pieces import King, Knight, Bishop


class EnoughPieces(FinishCondition):
    def process(self, ply: Ply, board: Board) -> None:
        self.pieces = sorted([list(map(lambda x: x.__class__, board.get_pieces(color=color,is_active=True))) for color in [Black(), White()]], key=len)

    def condition(self, ply: Ply, board: Board) -> bool:
        return self.pieces == [[King], [King]] or \
               self.pieces == [[King], [King, Knight]] or \
               self.pieces == [[King], [King, Bishop]]

    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        return Draw()
