from src.config.constants import BLACK_NAMES, PICK_COLOR_ERROR_MSG, WHITE, BLACK, BISHOP, BISHOP_NAMES, KING, KING_NAMES, KNIGHT, KNIGHT_NAMES, PAWN, PAWN_NAMES, QUEEN, QUEEN_NAMES, TOWER, TOWER_NAMES, WHITE_NAMES
from string import ascii_lowercase


def opposite_color(color: str) -> str:
    """
    If given black, returns white. If given white, returns black. In
    any other case, returns `None`.
    """
    if color == BLACK:
        return WHITE
    elif color == WHITE:
        return BLACK
    else:
        return None
        

def sum_tuple(tuple1: tuple, tuple2: tuple) -> tuple:
    """
    Sums two tuples component-wise.
    """
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])


def square_to_index(square: str) -> tuple:
    """
    Returns a tuple with integer cartesian coordinates for a chess square in algebraic notation.
    For example, `square_to_index('a2')` returns `(2,1)`.
    """
    result = None
    if square and len(square) == 2:
        col_str = square[0]
        row_str = square[1]
        if 'a' <= col_str <= 'h' and '1' <= row_str <= '8':
            result = (int(row_str), ascii_lowercase[0:8].index(col_str) + 1)
    return result


def is_valid_position(position: tuple) -> bool:
    """
    Checks if a tuple has its coordinates between 1 and 8 (both included).
    """
    return True if 1 <= position[0] <= 8 and 1 <= position[1] <= 8 else False


def get_piece_name(name: str) -> str:
    """
    This function standardizes the chess piece names.
    """
    if name in PAWN_NAMES:
        return PAWN
    elif name in KNIGHT_NAMES:
        return KNIGHT
    elif name in BISHOP_NAMES:
        return BISHOP
    elif name in TOWER_NAMES:
        return TOWER
    elif name in QUEEN_NAMES:
        return QUEEN
    elif name in KING_NAMES:
        return KING
    else:
        return None


def get_color(color: str):
    """
    This function standardizes the chess colors.
    """
    if color in WHITE_NAMES:
        return WHITE
    elif color in BLACK_NAMES:
        return BLACK
    else:
        return None