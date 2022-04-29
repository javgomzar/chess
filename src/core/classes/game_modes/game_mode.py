from abc import ABC, abstractmethod
from ..action_rules import ActionRule
from ..finish_conditions import FinishCondition
from ..error_classes.errors import InvalidMove
from ..rules import Rule
from ..pieces import Piece
from ..color import Color
from ..ply import Ply
from ..board import Board


class GameMode(ABC):
    rules: list[Rule]
    action_rules: list[ActionRule]
    finish_rules: list[FinishCondition]

    def __init__(self):
        self.connect_rules()

    def connect_rules(self) -> None:
        previous_rule = None
        for rule in self.rules:
            if previous_rule:
                previous_rule.set_next(rule)
            previous_rule = rule

    def get_valid_moves(self, piece: Piece, board: Board) -> list[tuple]:
        """
        Returns all valid moves for the piece in a given position.
        """        
        result = []
        from_position = board.get_position(piece)
        for possible_move in piece.available_positions(from_position):
            if self.validate(Ply(piece.color, from_position, possible_move), board):
                result.append(possible_move)
        return result
    
    def is_finished(self, ply: Ply, board: Board) -> bool:
        for piece in board.get_pieces(color=ply.color.opposite_color(), is_active=True):
            if len(self.get_valid_moves(piece, board)) > 0:
                return False
        else:
            return True
        try:
            self.finish_rules[0].handle(ply, board)
        except FinishState as final_state:
            if isinstance(final_state, Draw):
                ply.is_draw = True
            return True
            

    def validate(self, ply: Ply, board: Board) -> bool:
        try:
            self.rules[0].handle(ply, board)
            self.action_rules[0].handle(ply, board)
        except InvalidMove:
            return False
        except Exception as err:
            raise err
        else:
            return True
    
    @abstractmethod
    def init_board(self) -> Board:
        pass

    @abstractmethod
    def is_win(self, color: Color, board: Board) -> bool:
        pass
