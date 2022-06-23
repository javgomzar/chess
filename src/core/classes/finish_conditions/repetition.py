from ..handler import Handler
from ..pieces import Pawn
from ..board import Board
from ..ply import Ply

from .final_states import Draw, FinalState
from .finish_condition import FinishCondition


class Repetition(FinishCondition):
    counter : dict[str,int]

    def __init__(self) -> None:
        super(Handler).__init__()
        self.counter = {}

    def process(self, ply: Ply, board: Board) -> None:
        board_hash = str(board)
        last_piece = ply.piece
        if isinstance(last_piece, Pawn) or ply.taken_piece:
            self.counter = {}
        if board_hash in self.counter.keys():
            self.counter[board_hash] += 1
        else:
            self.counter[board_hash] = 1

    def condition(self, ply: Ply, board: Board) -> bool:
        board_hash = str(board)
        return self.counter[board_hash] == 3
        
    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        return Draw()
