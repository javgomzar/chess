from .pawn import Pawn
from .bishop import Bishop
from .rook import Rook
from .queen import Queen
from .king import King
from .knight import Knight


def piece_class_from_text(text: str) -> type:
        """
        This function standardizes the chess piece texts.
        """
        text = text.upper()
        if text in ["P","PAWN"]:
            return Pawn
        elif text in ["N","KNIGHT"]:
            return Knight
        elif text in ["B","BISHOP"]:
            return Bishop
        elif text in ["R","ROOK"]:
            return Rook
        elif text in ["Q","QUEEN"]:
            return Queen
        elif text in ["K","KING"]:
            return King
        else:
            return None
