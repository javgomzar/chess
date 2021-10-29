from src.core.classes.Piece import Piece


class Ply():
    """
    Class for a chess ply. A ply is basically a turn for a player; the word "ply" is
    used because a turn in chess consists usually of a pair of plies, one for each player.
    This class acts as a container.
    """
    start = None
    finish = None
    piece = None
    color = None
    action = None
    promotion = None
    is_check = False
    is_check_mate = False

    def __init__(self) -> None:
        pass

    def set_start(self, start: tuple):
        self.start = start
        return self

    def set_finish(self, finish: tuple):
        self.finish = finish
        return self
    
    def set_piece(self, piece: Piece): 
        self.piece = piece
        self.color = piece.color
        return self

    def set_action(self, action: str):
        self.action = action
        return self

    def set_check_mate(self):
        self.is_check_mate = True
        return self

    def set_check(self):
        self.is_check = True
        return self
    
    def set_promotion(self, piece_name):
        self.promotion = piece_name
        return self