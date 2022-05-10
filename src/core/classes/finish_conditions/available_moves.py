from ..position import Position
from ..finish_conditions import FinishCondition, FinalState, Draw, Win, Check
from ..board import Board
from ..ply import Ply


class AvailableMoves(FinishCondition):
    def __init__(self, game_mode: type) -> None:
        self._next = None
        self.game_mode = game_mode

    def process(self, ply: Ply, board: Board) -> None:
        self.opposite_color = ply.color.opposite_color()

    def condition(self, ply: Ply, board: Board) -> bool:
        if ply.from_position == Position.from_notation('f3') and ply.to_position == Position.from_notation('f7'):
            print('a')
            pass
        for piece in board.get_pieces(color=self.opposite_color, is_active=True):
            from_position = board.get_position(piece)
            for to_position in piece.available_positions(from_position):
                possible_ply = Ply(self.opposite_color, from_position, to_position)
                if self.game_mode.validate(possible_ply, board):
                    return False
        else:
            return True

    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        if Check.is_check(self.opposite_color, board):
            return Win()
        else:
            return Draw()
