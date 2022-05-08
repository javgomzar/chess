from .finish_condition import FinishCondition
from .finish_condition import FinishCondition
from .final_states import FinalState, Draw
from ..color import Black, White
from ..ply import Ply
from ..board import Board


class DeadPosition(FinishCondition):
    """This one is abstract as heck"""
    def process(self, ply: Ply, board: Board) -> None:
        self.black_pieces = board.get_pieces(Black(), is_active=True)
        self.white_pieces = board.get_pieces(White(), is_active=True)

        #TODO: Enough pieces; for example, king vs king, king vs king and knight, 
        # king and bishop or king and bishop and king and bishop with bishops of the same color

        #TODO: Kings are confined to each side of the board and nobody can check the other king
        pass

    def condition(self, ply: Ply, board: Board) -> bool:
        if len(self.black_pieces) == len(self.white_pieces) == 1:
            return True
        return False

    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        return Draw()
