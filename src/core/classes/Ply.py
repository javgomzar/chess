from dataclasses import dataclass, field
from typing import Optional
from src.core.classes.action import Action
from src.core.classes.color import Color
from src.core.classes.piece import Piece
from src.core.classes.position import Position


class Ply():
    """
    Class for a chess ply. A ply is basically a turn for a player; the word "ply" is
    used because a turn in chess consists usually of a pair of plies, one for each player.
    This class acts as a container.
    """
    action : Action
    from_position : Position
    to_position : Position
    piece : Piece
    color : Color
    gives_check : bool
    gives_check_mate : bool

    def __init__(self, from_position : Position, to_position: Position, piece: Piece, action: Action = None, is_check: bool = False, is_check_mate: bool = False) -> None:
        self.from_position = from_position
        self.to_position = to_position
        self.piece = piece
        self.color = piece.color
        self.action = action
        self.is_check = is_check
        self.is_check_mate = is_check_mate

    def set_action(self, action_class : type):
        self.action = action_class(self.from_position, self.to_position)
        return self

    def set_check_mate(self):
        self.is_check_mate = True
        return self

    def set_check(self):
        self.is_check = True
        return self
    
    def set_promotion(self, piece_class: type):
        self.promotion = piece_class
        return self