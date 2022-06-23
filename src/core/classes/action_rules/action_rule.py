from abc import abstractmethod

from ..error_classes import InvalidMove
from ..actions import Action
from ..rules import Rule
from ..ply import Ply
from ..board import Board


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
                print(f"Invalid move; '{self.__class__.__name__}' denied the ply from {ply.from_position} to {ply.to_position}.")
                raise InvalidMove(f"Invalid move; '{self.__class__.__name__}' denied the ply from {ply.from_position} to {ply.to_position}.")
        else:
            return
