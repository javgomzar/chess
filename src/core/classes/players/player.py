from abc import ABC, abstractmethod
from src.core.classes.color import Color
from src.core.classes.ply import Ply


class Player(ABC):
    color: Color

    @abstractmethod
    def input_ply(self) -> Ply:
        pass

    @abstractmethod
    def input_promotion(self) -> type:
        pass
