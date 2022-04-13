from typing import Protocol
from core.classes.actions.action import Action
from src.core.classes.ply import Ply
from src.core.classes.board import Board
from src.core.classes.board_controller import BoardController


class GameMode(Protocol):
    def init_board(self) -> Board:
        pass

    def get_action(self, ply: Ply, controller: BoardController) -> Action:
        pass

    def validate(self, action: Action, controller: BoardController) -> bool:
        pass

    def is_finished(self, controller: BoardController) -> bool:
        pass