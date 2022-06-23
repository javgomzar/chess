from .finish_conditions import FinalState, Draw, Win
from .rules import *
from .board import *
from .actions import *
from .ply import Ply
from .players import Player
from .game_modes import GameMode
from .color import *
from .board_view import BoardView


class Game():
    """
    Class for a chess game. To play, use the `play` method.
    """
    board: Board
    game_mode: GameMode
    is_finished: bool
    final_state: FinalState = None
    players: dict[Color, Player]
    board_view: BoardView

    def __init__(self, mode: GameMode, board_view: BoardView, player1: Player, player2: Player) -> None:
        if player1.color == player2.color:
            raise Exception("Players must have different colors")
        else:
            self.board = mode.init_board()
            self.game_mode = mode
            self.is_finished = False
            self.players = {}
            self.players[player1.color] = player1
            self.players[player2.color] = player2
            self.board_view = board_view

    def validate(self, ply: Ply) -> bool:
        return self.game_mode.validate(ply, self.board)
        
    def main_loop(self) -> None:
        while not self.is_finished:
            for color in [White(), Black()]:
                player = self.players[color]
                self.board_view.show_board(self.board)
                while True:
                    ply = player.input_ply(self.board)
                    if self.validate(ply):
                        break
                    else:
                        self.board_view.alert_invalid_move()

                if isinstance(ply.action, Promote):
                    ply.action.to_piece_class = player.input_promotion(self.board)
                    ply.action.is_filled = True
                
                self.board.execute(ply.action)

                opposite_player = self.players[color.opposite_color()]
                final_state = self.game_mode.is_finished(ply, self.board)
                if final_state:
                    self.is_finished = True
                    self.final_state = final_state
                    self.board_view.show_board(self.board)
                    if isinstance(final_state, Draw):
                        self.board_view.draw()
                        break
                    elif isinstance(final_state, Win):
                        self.board_view.win(player.color)
                        self.board_view.lose(opposite_player.color)
                        break
                elif ply.is_check:
                        self.board_view.alert_check()
