# APP
VERSION = "1.0.4"
APP_NAME = "CHESS"

# BOARD CONSTANTS
INIT_BOARD = {
    (8,1):{'piece':'T', 'color':'b'}, (8,2):{'piece':'N', 'color':'b'}, (8,3):{'piece':'B', 'color':'b'}, (8,4):{'piece':'Q', 'color':'b'}, (8,5):{'piece':'K', 'color':'b'}, (8,6):{'piece':'B', 'color':'b'}, (8,7):{'piece':'N', 'color':'b'}, (8,8):{'piece':'T', 'color':'b'},
    (7,1):{'piece':'P', 'color':'b'}, (7,2):{'piece':'P', 'color':'b'}, (7,3):{'piece':'P', 'color':'b'}, (7,4):{'piece':'P', 'color':'b'}, (7,5):{'piece':'P', 'color':'b'}, (7,6):{'piece':'P', 'color':'b'}, (7,7):{'piece':'P', 'color':'b'}, (7,8):{'piece':'P', 'color':'b'},
    (6,1):None, (6,2):None, (6,3):None, (6,4):None, (6,5):None, (6,6):None, (6,7):None, (6,8):None,
    (5,1):None, (5,2):None, (5,3):None, (5,4):None, (5,5):None, (5,6):None, (5,7):None, (5,8):None,
    (4,1):None, (4,2):None, (4,3):None, (4,4):None, (4,5):None, (4,6):None, (4,7):None, (4,8):None,
    (3,1):None, (3,2):None, (3,3):None, (3,4):None, (3,5):None, (3,6):None, (3,7):None, (3,8):None,
    (2,1):{'piece':'P', 'color':'w'}, (2,2):{'piece':'P', 'color':'w'}, (2,3):{'piece':'P', 'color':'w'}, (2,4):{'piece':'P', 'color':'w'}, (2,5):{'piece':'P', 'color':'w'}, (2,6):{'piece':'P', 'color':'w'}, (2,7):{'piece':'P', 'color':'w'}, (2,8):{'piece':'P', 'color':'w'},
    (1,1):{'piece':'T', 'color':'w'}, (1,2):{'piece':'N', 'color':'w'}, (1,3):{'piece':'B', 'color':'w'}, (1,4):{'piece':'Q', 'color':'w'}, (1,5):{'piece':'K', 'color':'w'}, (1,6):{'piece':'B', 'color':'w'}, (1,7):{'piece':'N', 'color':'w'}, (1,8):{'piece':'T', 'color':'w'},
}

EMPTY_BOARD_STRING = "  ╔════╤════╤════╤════╤════╤════╤════╤════╗\n" + \
                     "8 ║ 81 │ 82 │ 83 │ 84 │ 85 │ 86 │ 87 │ 88 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "7 ║ 71 │ 72 │ 73 │ 74 │ 75 │ 76 │ 77 │ 78 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "6 ║ 61 │ 62 │ 63 │ 64 │ 65 │ 66 │ 67 │ 68 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "5 ║ 51 │ 52 │ 53 │ 54 │ 55 │ 56 │ 57 │ 58 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "4 ║ 41 │ 42 │ 43 │ 44 │ 45 │ 46 │ 47 │ 48 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "3 ║ 31 │ 32 │ 33 │ 34 │ 35 │ 36 │ 37 │ 38 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "2 ║ 21 │ 22 │ 23 │ 24 │ 25 │ 26 │ 27 │ 28 ║\n" + \
                     "  ╟────┼────┼────┼────┼────┼────┼────┼────╢\n" + \
                     "1 ║ 11 │ 12 │ 13 │ 14 │ 15 │ 16 │ 17 │ 18 ║\n" + \
                     "  ╚════╧════╧════╧════╧════╧════╧════╧════╝\n" + \
                     "    a    b    c    d    e    f    g    h   "

# STANDARD VALUES
BLACK = "Black"
BLACK_NAMES = [BLACK, 'black', 'b', 'B', 'BLACK', 'Black']
WHITE = "White"
WHITE_NAMES = [WHITE, 'white', 'w', 'W', 'WHITE', 'White']
PAWN = "PAWN"
PAWN_NAMES = ["pawn", "p", "P", "Pawn", "PAWN"]
KNIGHT = "KNIGHT"
KNIGHT_NAMES = ["knight", "n", "N", "Knight", "KNIGHT"]
BISHOP = "BISHOP"
BISHOP_NAMES = ["bishop", "b", "B", "Bishop", "BISHOP"]
TOWER = "TOWER"
TOWER_NAMES = ["tower", "t", "T", "Tower", "TOWER"]
QUEEN = "QUEEN"
QUEEN_NAMES = ["queen", "q", "Q", "Queen", "QUEEN"]
KING = "KING"
KING_NAMES = ["king", "k", "K", "King", "KING"]
LEFT = 'L'
RIGHT = 'R'
MOVE = 'M'
EN_PASSANT = 'EP'
PROMOTE = 'P'
CASTLE = 'C'

# Unicode representation
UNICODE_DICT = {
    BLACK: {
        KING: "\u265A",
        QUEEN: "\u265B",
        TOWER: "\u265C",
        BISHOP: "\u265D",
        KNIGHT: "\u265E",
        PAWN: "\u265F"
    },
    WHITE: {
        KING: "\u2654", 
        QUEEN: "\u2655",
        TOWER: "\u2656",
        BISHOP: "\u2657",
        KNIGHT: "\u2658",
        PAWN: "\u2659"
    }
}

# Messages
PICK_COLOR_MSG = f"Pick a color ('{BLACK}' or '{WHITE}'): "
PICK_COLOR_ERROR_MSG = f"That's not {BLACK} or {WHITE}."
INVALID_MOVE_MSG = "The move selected is not valid."
CHOOSE_PIECE_MSG = "Pick a piece to move: "
CHOOSE_MOVE_MSG = "Pick a square to move that piece: "
INVALID_COLOR_MSG = "The piece you chose is not yours."
EMPTY_SQ_MSG = "The square you chose is empty."
INVALID_SQ = "Invalid square input. Pick a letter between 'a' and 'h', and a number between 1 and 8; for example: e2."
INCOMPLETE_TURN_ERROR = "A turn was tried to be added without the last one being complete"
INVALID_PIECE = "The piece has a non valid type."
INVALID_PROMOTION = "That's not a valid piece to promote."
INVALID_ACTION = "Invalid action."

# Move lists
KNIGHT_MOVES = [(2,1),(1,2),(1,-2),(-1,2),(2,-1),(-1,-2),(-2,1),(-2,-1)]
BISHOP_DIRECTIONS = [(1,1),(1,-1),(-1,1),(-1,-1)]
TOWER_DIRECTIONS = [(0,1),(0,-1),(-1,0),(0,-1)]
QUEEN_DIRECTIONS = BISHOP_DIRECTIONS + TOWER_DIRECTIONS
DIRECTIONS = {
    BISHOP: BISHOP_DIRECTIONS,
    TOWER: TOWER_DIRECTIONS,
    QUEEN: QUEEN_DIRECTIONS
}

# Paths & Filenames
LOCAL_PATH = "D:/Code/Python/chess/"
MEDIA_PATH = LOCAL_PATH +"media/"
IMG_DICT = {
    BLACK: {
        PAWN: LOCAL_PATH + "media/Black/Pawn.png",
        KNIGHT: LOCAL_PATH + "media/Black/Knight.png",
        BISHOP: LOCAL_PATH + "media/Black/Bishop.png",
        TOWER: LOCAL_PATH + "media/Black/Tower.png",
        QUEEN: LOCAL_PATH + "media/Black/Queen.png",
        KING: LOCAL_PATH + "media/Black/King.png"
    },
    WHITE: {
        PAWN: LOCAL_PATH + "media/White/Pawn.png",
        KNIGHT: LOCAL_PATH + "media/White/Knight.png",
        BISHOP: LOCAL_PATH + "media/White/Bishop.png",
        TOWER: LOCAL_PATH + "media/White/Tower.png",
        QUEEN: LOCAL_PATH + "media/White/Queen.png",
        KING: LOCAL_PATH + "media/White/King.png"
    }
}

BOARD_IMG = LOCAL_PATH + "media/Board.png"
TMP_FILENAME = "tmp.png"
TMP_PATH = LOCAL_PATH + "media/tmp/" + TMP_FILENAME

# Regular Expressions
SQ_RE = "([a-h,A-H][1-8])"
MOVE_RE = "([a-h,A-H][1-8]).*([a-h,A-H][1-8])"
PIECE_RE =  "([K,Q,T,B,N])([a-h][1-8])"