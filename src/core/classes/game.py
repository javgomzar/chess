from .rules import *
from .board import *
from .actions import *
from src.core.classes.ply import Ply
from src.core.classes.players.player import Player
from src.core.classes.game_modes.game_mode import GameMode
from .color import Black, Color, White



class Game():
    """
    Class for a chess game. To play, use the `play` method.
    """
    board: Board
    game_mode: GameMode
    is_finished: bool
    players: dict[Color, Player]

    def __init__(self, mode: GameMode, player1: Player, player2: Player) -> None:
        if player1.color == player2.color:
            raise Exception("Players must have different colors")
        else:
            self.board = mode.init_board()
            self.game_mode = mode
            self.is_finished = False
            self.players = {}
            self.players[player1.color] = player1
            self.players[player2.color] = player2
    
    def get_action(self, ply: Ply) -> Action:
        return self.game_mode.get_action(ply, self.board)

    def validate(self, ply: Ply) -> bool:
        return self.game_mode.validate(ply, self.board)
        
    def main_loop(self) -> None:
        while not self.is_finished:
            for color in [White(), Black()]:
                player = self.players[color]
                player.show_board(self.board)
                while True:
                    ply = player.input_ply(color)
                    if self.validate(ply):
                        break
                    else:
                        player.invalid_move()

                if isinstance(ply.action, Promote):
                    ply.action.to_piece_class = player.input_promotion(self.board)
                
                self.board.execute(ply.action)

                opposite_player = self.players[color.opposite_color()]
                if self.game_mode.is_finished(ply, self.board):
                    self.is_finished = True
                    player.show_board(self.board)
                    opposite_player.show_board(self.board)
                    if ply.is_draw:
                        player.draw()
                        opposite_player.draw()
                        break
                    else:
                        player.win()
                        opposite_player.lose()
                        break
                elif ply.is_check:
                        player.alert_check()
                        opposite_player.alert_check()
