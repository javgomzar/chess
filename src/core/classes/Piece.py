from src.config.constants import UNICODE_DICT
from src.core.utils import get_piece_name, get_color


class Piece():
    """
    Class for a chess piece. The piece type is in the attribute `name`. Each
    piece has a unique `id` to be able to distinguish between pieces of the
    same color and type.
    """
    __lastId = 1
    color = None
    name = None

    def __init__(self, name, color) -> None:

        self.id = self.__lastId
        Piece.__lastId += 1

        self.color = get_color(color)
        self.name = get_piece_name(name)


    def __str__(self) -> str:
        if self.color and self.name:
            return UNICODE_DICT[self.color][self.name]
        else:
            return "  "


    def __repr__(self) -> str:
        return f"<Piece: {self.color} {self.name} {self.id}>"


    def __bool__(self) -> bool:
        return True
