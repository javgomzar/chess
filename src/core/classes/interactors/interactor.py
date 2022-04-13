from abc import ABC, abstractmethod
from src.core.classes.color import Black, Color, White
from core.classes.players.player import Player
from src.core.classes.board import Board


class Interactor(ABC):
    players: dict[Color, Player]

    def __init__(self, white_player: Player, black_player: Player) -> None:
        self.players[Black()] = black_player
        self.players[White()] = white_player

    @abstractmethod
    def show_board(self, board: Board) -> None:
        pass
