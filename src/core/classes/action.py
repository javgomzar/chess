from typing import Protocol
from src.core.classes.board import Board


class Action(Protocol):
    def execute(self, board : Board) -> None:
        pass

    def undo(self, board : Board) -> None:
        pass

    def redo(self, board : Board) -> None:
        pass

