from abc import abstractmethod
from ..board import Board
from ..color import Color


class BoardView:
    """
    Class that manages how to view a board.
    """
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

    @abstractmethod
    def invalid_move(self) -> None:
        pass
