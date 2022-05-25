from abc import abstractmethod
from typing import Protocol
from ..pieces import PieceManager


class Action(Protocol):
    @abstractmethod
    def process(self, piece_manager: PieceManager) -> None:
        pass
    
    @abstractmethod
    def execute(self, piece_manager: PieceManager) -> None:
        pass

    @abstractmethod
    def undo(self, piece_manager: PieceManager) -> None:
        pass

    @abstractmethod
    def redo(self, piece_manager: PieceManager) -> None:
        pass
