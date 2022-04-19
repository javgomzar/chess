from abc import ABC, abstractmethod
from src.core.classes.pieces.queen import Queen
from src.core.classes.color import Color
from src.core.classes.board import Board
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
    def loose(self) -> None:
        pass

    @abstractmethod
    def input_ply(self, board: Board) -> Ply:
        pass

    @abstractmethod
    def input_promotion(self, board: Board) -> type:
        return Queen
