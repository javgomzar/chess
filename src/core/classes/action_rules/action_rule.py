from abc import abstractmethod
from ..error_classes import InvalidMove
from ..actions import Action
from ..rules import Rule
from ..ply import Ply
from ..board import Board
import logging

class ActionRule(Rule):
    def process(self, ply: Ply, board: Board) -> None:
        if not ply.action:
            is_valid = self.validate(ply, board)
            if is_valid:
                ply.action = self.get_action(ply)

    @abstractmethod
    def get_action(self, ply: Ply) -> Action:
        pass

    def handle(self, ply: Ply, board: Board) -> None:
        self.process(ply, board)
        if isinstance(self._next, ActionRule) or (self._next and ply.action):
            self._next.handle(ply, board)
        elif not ply.action:
                logging.debug(f"Invalid move; '{self.__class__.__name__}' denied the ply.")
                raise InvalidMove()
        else:
            return

    # def handle(self, ply: Ply, board: Board) -> None:
    #     is_valid = self.validate(ply, board)
    #     if is_valid:
    #         ply.action = self.get_action(ply)
    #         return
    #     else:
    #         if self._next:
    #             self._next.handle(ply, board)
    #         else:
    #             logging.debug(f"Invalid move; '{self.__class__.__name__}' denied the ply.")
    #             raise InvalidMove()
