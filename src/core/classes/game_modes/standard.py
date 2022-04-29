from ..finish_conditions.fifty_moves import FinishCondition, FiftyMoves
from ..action_rules import *
from ..board import *
from ..pieces import *
from ..rules import *
from ..action_rules import *
from ..color import *
from ..finish_conditions import *
from .game_mode import GameMode


class Standard(GameMode):
    rules : list[Rule] = [ValidColor(), ValidPieceMove(), TakeOwnPiece(), Block(), Pin()]
    action_rules : list[ActionRule] = [PromoteRule(), EnPassantRule(), CastleRule(), MoveRule()]
    finish_conditions : list[FinishCondition] = [Repetition(), FiftyMoves(), Check()]

    def init_board(self) -> Board:
        board = Board()
        for color in [Black(), White()]:
                for col,class_pair in enumerate(zip([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook], [Pawn]*8)):
                    for row,piece_class in zip((color.king_row, color.pawn_row), class_pair):
                        board.add(piece_class(color), Position(col,row))
        return board

    # def validate(self, ply: Ply, board: Board) -> bool:
    #     """
    #     Validates a ply for the current board and a previous board. Returns `True` if the ply is valid
    #     and `False` if it's not valid. If the ply is valid, this method fills the action attribute for
    #     the ply.
    #     """
    #     piece = board.get_piece(ply.from_position)

    #     if not piece.can_move(ply.vector):
    #         return False
        
    #     ply.action = self.get_action(ply, board)

    #     current_board = board.copy()
    #     piece_taken = current_board.get_piece(ply.to_position)

    #     # Exclude taking your own piece, pins and blocks
    #     if piece_taken and piece_taken.color == ply.color or \
    #        not isinstance(piece, Knight) and self.is_blocked(ply, current_board) or \
    #        self.is_pinned(ply, board):
    #         return False

    #     # Pawns can only move diagonally under certain conditions
    #     elif isinstance(piece, Pawn):
    #         if piece_taken:
    #             if (isinstance(ply.action, Move) or isinstance(ply.action, Promote)) and \
    #                 piece.is_capture(ply.to_position - ply.from_position):
    #                 return True
    #             else:
    #                 return False
    #         elif isinstance(ply.action, EnPassant) or not piece.is_capture(ply.to_position - ply.from_position):
    #             return True
    #         else:
    #             return False           

    #     # Can't castle if there is a check in the way
    #     if isinstance(ply.action, Castle):
    #         pointer = ply.color.king_position
    #         direction = ply.action.direction
    #         for n in range(0,2):
    #             pointer += direction
    #             possible_board = board.try_action(Move(piece, direction))
    #             if self.is_check(ply.color, possible_board):
    #                 return False
    #     return True

    def is_win(self, color: Color, board: Board):
        return Check.is_check(color.opposite_color(), board)
