from dataclasses import dataclass
from src.core.classes.color import Color
from src.core.classes.position import Position


@dataclass
class Ply:
    """
    Class for a chess ply. This class acts as a container.
    """
    color : Color
    from_position : Position
    to_position : Position
