from dataclasses import dataclass, field

from .actions import Action
from .pieces import Piece
from .color import Color
from .position import Position
from .vector import Vector


@dataclass
class Ply:
    """
    Class for a chess ply. This class acts as a container.
    """

    color : Color = field(init=True)
    from_position : Position = field(init=True)
    to_position : Position = field(init=True)
    vector: Vector = field(init=False)
    piece: Piece = field(init=False, default=None)
    taken_piece: Piece = field(init=False, default=None)
    is_check : bool = field(init=False, default=False)
    is_draw : bool = field(init=False, default=False)
    is_finished : bool = field(init=False, default=False)
    action: Action = field(init=False, default=None)
    is_valid : bool = field(init=False, default=None)

    def __post_init__(self):
        self.vector = self.to_position - self.from_position
