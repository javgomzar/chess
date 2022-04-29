from ..handler import Handler
from .finish_condition import FinishCondition
from ..pieces import Pawn
from ..board import Board
from .finish_states.draw import Draw
from ..ply import Ply


class Repetition(FinishCondition):
    counter : dict[str,int]

    def __init__(self) -> None:
        super(Handler).__init__()
        self.counter = {}

    def condition(self, ply: Ply, board: Board) -> bool:
        self.update_counter(ply, board)
        return self.counter[board] == 3

    def update_counter(self, ply: Ply, board: Board) -> None:
        last_piece = ply.piece
        if isinstance(last_piece, Pawn) or ply.taken_piece:
            self.counter = {}
        elif board in self.counter.keys():
            self.counter[board] += 1
        else:
            self.counter[board] = 1

    def handle(self, ply: Ply, board: Board) -> None:
        
        if self.condition():
            return 
        if self._next:
            self._next.handle(board)
        else:
            return

