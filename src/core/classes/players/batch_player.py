from ..pieces import Queen
from .player import Player
from ..color import Color
from ..ply import Ply
from ..board import Board

class BatchPlayer(Player):
    def __init__(self, color: Color, ply_list: list[Ply]):
        self.color = color
        self.ply_list = ply_list
        self.index = 0

    def input_ply(self, board: Board) -> Ply:
        self.index += 1
        return self.ply_list[self.index-1]

    def input_promotion(self, board: Board) -> type:
        return Queen

    def reset(self):
        self.index = 0
