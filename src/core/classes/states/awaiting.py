from dataclasses import dataclass
from src.core.classes.states.state import State
from src.core.classes.board import Board
from src.core.classes.players.player import Player
from src.core.classes.color import Color

@dataclass
class Awaiting:
    board: Board
    player: Player

    def handle(self):
        
