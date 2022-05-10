from abc import abstractmethod
import logging
from ..handler import Handler
from ..ply import Ply
from .final_states import FinalState
from ..board import Board


class FinishCondition(Handler):
    @abstractmethod
    def process(self, ply: Ply, board: Board) -> None:
        pass

    @abstractmethod
    def condition(self, ply: Ply, board: Board) -> bool:
        pass

    @abstractmethod
    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        pass

    def handle(self, ply: Ply, board: Board) -> FinalState:
        self.process(ply, board)
        if self.condition(ply, board):
            logging.debug(f"Game ended because of finish condition {self.__class__.__name__}")
            return self.get_final_state(ply, board)
        elif self._next:
            return self._next.handle(ply, board)
        else:
            return None
