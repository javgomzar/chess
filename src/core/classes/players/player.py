from abc import ABC, abstractmethod
from ..color import Color
from ..board import Board
from ..pieces import Queen
from src.core.classes.ply import Ply


class Player(ABC):
    color: Color

    def __init__(self, color: Color):
        self.color = color

    @abstractmethod
    def show_board(self, board: Board) -> None:
        pass

    @abstractmethod
    def invalid_move(self) -> None:
        pass

    @abstractmethod
    def alert_check(self) -> None:
        pass

    @abstractmethod
    def win(self) -> None:
        pass

    @abstractmethod
    def lose(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def input_ply(self, board: Board) -> Ply:
        pass

    @abstractmethod
    def input_promotion(self, board: Board) -> type:
        return Queen
