from ..pieces import Queen
from .player import Player
from ..color import Color
from ..ply import Ply
from ..board import Board
from ..error_classes import InvalidMove

class BatchPlayer(Player):
    def __init__(self, color: Color, ply_list: list[Ply]):
        self.color = color
        self.ply_list = ply_list
        self.index = 0

    def show_board(self, board: Board) -> None:
        print(board)

    def invalid_move(self) -> None:
        raise InvalidMove()

    def alert_check(self) -> None:
        print("Check!")

    def win(self) -> None:
        print(f"{self.color} wins")

    def lose(self) -> None:
        print(f"{self.color} looses")

    def draw(self) -> None:
        print("Draw")

    def input_ply(self, board: Board) -> Ply:
        self.index += 1
        return self.ply_list[self.index-1]

    def input_promotion(self, board: Board) -> type:
        return Queen
