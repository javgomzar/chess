from src.config.constants import BLACK, WHITE
from .Ply import Ply

class Turn():

    plies : list

    def __init__(self) -> None:
        self.plies = []

    def __iter__(self) -> list:
        return self.plies

    def add_ply(self, ply: Ply) -> bool:
        if len(self.plies) == 0:
            if ply.color != WHITE:
                raise ValueError(f"First ply in turn is not {WHITE}.")
            else:
                self.plies.append(ply)
                return True
        elif len(self.plies) == 1:
            if ply.color != BLACK:
                raise ValueError(f"Second ply in turn is not {BLACK}.")
            else:
                self.plies.append(ply)
                return True
        else:
            return False
