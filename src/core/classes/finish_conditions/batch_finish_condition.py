from ..ply import Ply
from ..board import Board

from .finish_condition import FinishCondition


class BatchFinishCondition(FinishCondition):
    stack: list[FinishCondition]

    def process(self, ply: Ply, board: Board) -> None:
        for finish_condition in self.stack:
            finish_condition.process(ply, board)

    def condition(self, ply: Ply, board: Board) -> bool:
        for finish_condition in self.stack:
            if finish_condition.condition(ply, board):
                return True
        else:
            return False
