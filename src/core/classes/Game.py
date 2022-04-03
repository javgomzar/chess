from core.classes.board_controller import BoardController
from src.config.constants import BISHOP, BLACK, BLACK_NAMES, EMPTY_SQ_MSG, INVALID_COLOR_MSG, INVALID_PROMOTION, INVALID_SQ, KNIGHT, INVALID_MOVE_MSG, PICK_COLOR_ERROR_MSG, PICK_COLOR_MSG, PROMOTE, QUEEN, TOWER, WHITE, WHITE_NAMES
from src.core.classes.action import Promote
from src.core.classes.color import Black, Color, White
from src.core.classes.input_manager import InputManager
from src.core.classes.board import Board
from src.core.classes.position import PositionError
from src.core.classes.rules import Rules
from src.core.classes.ply import Ply
import copy


class Game(InputManager):
    """
    Class for a chess game. To play, use the `play` method.
    """
    def __init__(self) -> None:
        self.controller = BoardController()
        self.is_finished = False

    def add_ply(self, ply: Ply):
        """
        Adds a ply to the history of the game if it's valid, and executes its action.
        """
        if len(self.plies) > 0:
            self.plies[-1].action.execute(self.previous_board)
        self.plies.append(ply)
        ply.action.execute(self.board)

    def validate_add_ply(self, ply: Ply):
        if self.is_finished or (len(self.plies) == 0 and ply.color != WHITE) \
                            or (len(self.plies) > 0 and ply.color == self.plies[-1].color):
            return False
        elif Rules().validate(ply, self.board, self.previous_board):
            if isinstance(ply.action, Promote) and not ply.promotion:
                return False
            self.add_ply(ply)
            if Rules().is_finished(self.board, self.previous_board, ply.color.opposite_color()):
                self.is_finished = True
            return True
        else:
            return False

    def play(self):
        """
        Play a chess game controling both players.
        """
        print(self.board)
        
        # Main loop
        while not self.is_finished:
            for color in [White(), Black()]:
                # Input loop
                while True:
                    ply = self.ply_input(color)
                    if not Rules().validate(ply, self.board, self.previous_board):
                        print(INVALID_MOVE_MSG)
                    elif isinstance(ply.action, Promote):
                        ply.set_promotion(self.promotion_input())
                        break
                    else:
                        break
                
                # Add the ply to the history
                self.add_ply(ply)
                
                # Print board
                print(self.board)

                # Checks
                is_check = Rules().is_check(self.board, color.opposite_color())
                if is_check:
                    print("Check!")
                
                # Finishing condition
                if Rules().is_finished(self.board, self.previous_board, color.opposite_color()):
                    self.is_finished = True
                    if is_check:
                        print(f"{color} won!")
                    else:
                        print("It's a draw!")
                    break

