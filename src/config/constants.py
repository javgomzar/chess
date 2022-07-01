# APP
VERSION = "1.0.4"
APP_NAME = "CHESS"


# Color text
BLACK = "Black"
WHITE = "White"


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


# Paths & Filenames
LOCAL_PATH = "D:/Code/Python/chess/"
MEDIA_PATH = LOCAL_PATH +"media/"

TMP_FILENAME = "tmp.png"
TMP_PATH = LOCAL_PATH + "media/tmp/" + TMP_FILENAME
