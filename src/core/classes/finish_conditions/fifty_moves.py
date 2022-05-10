from ..pieces.pawn import Pawn
from ..handler import Handler
from .finish_condition import FinishCondition
from .final_states import FinalState, Draw
from ..ply import Ply
from ..board import Board

class FiftyMoves(FinishCondition):
    def __init__(self) -> None:
        super(Handler).__init__()
        self.count = 0

    def process(self, ply: Ply, board: Board) -> None:
        if not ply.taken_piece and not isinstance(ply.piece, Pawn):
            self.count += 1
        else:
            self.count = 0

    def condition(self, ply: Ply, board: Board) -> bool:
        return self.count == 50

    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        return Draw()
