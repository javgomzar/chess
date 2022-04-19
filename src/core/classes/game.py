from src.core.classes.actions.action import Action
from src.core.classes.ply import Ply
from src.core.classes.players.player import Player
from src.core.classes.game_modes.game_mode import GameMode
from src.core.classes.board_controller import BoardController
from src.config.constants import INVALID_MOVE_MSG
from src.core.classes.actions import Promote
from src.core.classes.color import Black, Color, White
from src.core.classes.input import Input
from src.core.classes.rules import Rules


class Game():
    """
    Class for a chess game. To play, use the `play` method.
    """
    controller: BoardController
    game_mode: GameMode
    is_finished: bool
    players: dict[Color, Player]

    def __init__(self, mode: GameMode, player1: Player, player2: Player) -> None:
        if player1.color == player2.color:
            raise Exception("Players must have different colors")
        else:
            self.controller = BoardController(mode.init_board())
            self.game_mode = mode
            self.is_finished = False
            self.players = {}
            self.players[player1.color] = player1
            self.players[player2.color] = player2
    
    def get_action(self, ply: Ply) -> Action:
        return self.game_mode.get_action(ply, self.controller)

    def validate(self, ply: Ply) -> bool:
        return self.game_mode.validate(ply, self.controller)

    def main_loop(self) -> None:
        while not self.is_finished:
            for color in [White(), Black()]:
                player = self.players[color]
                player.show_board(self.controller.board)
                while True:
                    ply = player.input_ply(color)
                    ply.action = self.get_action(ply)
                    if self.validate(ply):
                        break
                    else:
                        player.invalid_move()

                if isinstance(ply.action, Promote):
                    ply.action.to_piece_class = player.input_promotion(self.controller.get_board())
                
                self.controller.execute(ply.action)

                if self.game_mode.is_check(color, self.controller.get_board()):
                    player.alert_check()

                if self.game_mode.is_finished(color.opposite_color(), self.controller):
                    self.is_finished = True
                    if self.game_mode.is_win(color, self.controller):
                        player.win()
                        self.players[color.opposite_color()].loose()
                    elif self.game_mode.is_win(color.opposite_color()):
                        print('ª')

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
                
                # If pawn is promoting, choose piece to promote to
                if isinstance(ply.action, Promote):
                    ply.action.choose()
                    
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

