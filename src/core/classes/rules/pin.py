from ..finish_conditions import Check
from ..board import Board, Move
from ..ply import Ply
from .rule import Rule


class Pin(Rule):
    def process(self, ply: Ply, board: Board) -> None:
        return

    @classmethod
    def validate(self, ply: Ply, board: Board) -> bool:
        move = Move(ply.piece, ply.vector)
        possible_board = board.try_action(move)
        if Check.is_check(ply.color, possible_board):
            return False
        else:
            return True
