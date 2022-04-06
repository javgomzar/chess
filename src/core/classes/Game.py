from src.core.classes.board_controller import BoardController
from src.config.constants import INVALID_MOVE_MSG, WHITE
from src.core.classes.actions import Promote
from src.core.classes.color import Black, White
from src.core.classes.input import Input
from src.core.classes.rules import Rules
from src.core.classes.ply import Ply


class Game():
    """
    Class for a chess game. To play, use the `play` method.
    """
    def __init__(self) -> None:
        self.controller = BoardController()
        self.is_finished = False

    # def add_ply(self, ply: Ply):
    #     """
    #     Adds a ply to the history of the game if it's valid, and executes its action.
    #     """
    #     if len(self.plies) > 0:
    #         self.plies[-1].action.execute(self.previous_board)
    #     self.plies.append(ply)
    #     ply.action.execute(self.board)

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
        print(self.controller.board)
        
        # Main loop
        while not self.is_finished:
            for color in [White(), Black()]:
                # Input loop
                while True:
                    ply = Input.ply(color, self.controller.board)
                    if not Rules().validate(ply, self.controller):
                        print(INVALID_MOVE_MSG)
                    else:
                        break
                
                # Execute ply action
                self.controller.execute(ply.action)

                # Print board
                print(self.controller.board)

                # Checks
                is_check = Rules().is_check(color.opposite_color(), self.controller.board)
                if is_check:
                    print("Check!")
                
                # Finishing condition
                if Rules().is_finished(color.opposite_color(), self.controller):
                    self.is_finished = True
                    if is_check:
                        print(f"{color} won!")
                    else:
                        print("It's a draw!")
                    break

