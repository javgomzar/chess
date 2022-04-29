from abc import abstractclassmethod
from ..handler import Handler
from ..error_classes.errors import InvalidMove
from ..board import Board
from ..ply import Ply
import logging


class Rule(Handler):
    @abstractclassmethod
    def validate(self, ply: Ply, board: Board) -> bool:
        pass

    def handle(self, ply: Ply, board: Board) -> None:
        is_valid = self.validate(ply, board)
        if is_valid:
            if self._next:
                self._next.handle(ply, board)
            else:
                return
        else:
            logging.debug(f"Invalid move. '{self.__class__.__name__}' denied the ply.")
            raise InvalidMove()
