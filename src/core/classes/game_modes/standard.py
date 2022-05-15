from ..error_classes import InvalidMove
from ..action_rules import *
from ..board import *
from ..pieces import *
from ..rules import *
from ..action_rules import *
from ..color import *
from ..finish_conditions import *
from ..ply import Ply
from .game_mode import GameMode


class Standard(GameMode):
    rules : list[Rule] = [ValidColor(), ValidPieceMove(), TakeOwnPiece(), Block(), Pin()]
    action_rules : list[ActionRule] = [PromoteRule(), EnPassantRule(), CastleRule(), MoveRule()]
    finish_conditions : list[FinishCondition] 

    def __init__(self):
        self.finish_conditions = [Repetition(), FiftyMoves(), DeadPosition(), AvailableMoves(self.__class__)]
        self.connect_rules()

    def connect_rules(self) -> None:
        for list_of_rules in [self.rules, self.action_rules, self.finish_conditions]:
            previous_rule = None
            for rule in list_of_rules:
                if previous_rule:
                    previous_rule.set_next(rule)
                previous_rule = rule

    @classmethod
    def init_board(self) -> Board:
        board = Board()
        for color in [Black(), White()]:
                for col,class_pair in enumerate(zip([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook], [Pawn]*8)):
                    for row,piece_class in zip((color.king_row, color.pawn_row), class_pair):
                        board.add(piece_class(color), Position(col,row))
        return board

    @classmethod
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

    def is_finished(self, ply: Ply, board: Board) -> FinalState:
            final_state = self.finish_conditions[0].handle(ply, board)
            if final_state:
                return final_state
