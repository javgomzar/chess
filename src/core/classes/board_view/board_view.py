from abc import abstractmethod, ABC

from ..game_modes import GameMode
from ..board import Board
from ..color import Color


class BoardView(ABC):
    """
    Class that manages how to view a board.
    """
    game_mode: GameMode
    
    def __init__(self, game_mode: GameMode) -> None:
        self.game_mode = game_mode

    @abstractmethod
    def show_board(self, board: Board) -> None:
        pass

    @abstractmethod
    def alert_check(self) -> None:
        pass

    @abstractmethod
    def alert_invalid_move(self) -> None:
        pass

    @abstractmethod
    def win(self, color: Color) -> None:
        pass

    @abstractmethod
    def lose(self, color: Color) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
