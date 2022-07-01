from abc import ABC, abstractmethod

from ..color import Color
from ..board import Board
from ..pieces import Queen
from ..ply import Ply


class Player(ABC):
    color: Color

    def __init__(self, color: Color):
        self.color = color

    @abstractmethod
    def input_ply(self, board: Board) -> Ply:
        pass

    @abstractmethod
    def input_promotion(self, board: Board) -> type:
        return Queen
