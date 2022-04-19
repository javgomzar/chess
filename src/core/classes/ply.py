from dataclasses import dataclass, field
from src.core.classes.color import Color
from src.core.classes.position import Position, Vector


@dataclass
class Ply:
    """
    Class for a chess ply. This class acts as a container.
    """
    color : Color
    from_position : Position
    to_position : Position
    vector: Vector = field(init=False)

    def __post_init__(self):
        self.vector = self.to_position - self.from_position
