from .enough_pieces import EnoughPieces
from .finish_condition import FinishCondition
from .batch_finish_condition import BatchFinishCondition
from .final_states import FinalState, Draw
from .locked_kings import LockedKings
from ..ply import Ply
from ..board import Board


class DeadPosition(BatchFinishCondition):
    """
    Finishes the game if a dead position has been reached. This includes
    when no mates are possible due to a lack of pieces, or if the kings are
    locked to each side of the board.
    """
    stack : list[FinishCondition] = [EnoughPieces(), LockedKings()]

    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        return Draw()
