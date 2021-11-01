from src.config.constants import BISHOP, BLACK, BLACK_NAMES, EMPTY_SQ_MSG, INVALID_COLOR_MSG, INVALID_PROMOTION, INVALID_SQ, KNIGHT, MOVE_NOT_VALID, PICK_COLOR_ERROR_MSG, PICK_COLOR_MSG, PROMOTE, QUEEN, TOWER, WHITE, WHITE_NAMES
from src.core.utils import get_piece_name, opposite_color, square_to_index
from .Board import Board
from .Rules import Rules
from .Ply import Ply
import copy


class Game():
    """
    Class for a chess game. To play, use the `play` method.
    """
    def __init__(self) -> None:
        self.plies = []
        self.board = Board().init_std_board()
        self.previous_board = copy.deepcopy(self.board)
        self.is_finished = False


    def add_ply(self, ply: Ply):
        """
        Adds a ply to the history of the game if it's valid, and executes its action.
        """
        if len(self.plies) > 0:
            self.previous_board.execute_action(self.plies[-1])
        self.plies.append(ply)
        self.board.execute_action(ply)

    def validate_add_ply(self, ply: Ply):
        if self.is_finished or (len(self.plies) == 0 and ply.color != WHITE) \
                            or (len(self.plies) > 0 and ply.color == self.plies[-1].color):
            return False
        elif Rules().validate(ply, self.board, self.previous_board):
            if ply.action == PROMOTE and not ply.promotion:
                return False
            self.add_ply(ply)
            if Rules().is_finished(self.board, self.previous_board, opposite_color(ply.color)):
                self.is_finished = True
            return True
        else:
            return False

    def play(self):
        """
        Play a chess game controling both players.
        """
        print(self.board)
        
        # Main loop
        while not self.is_finished:
            for color in [WHITE, BLACK]:
                # Input loop
                while True:
                    ply = self.ply_input(color)
                    if not Rules().validate(ply, self.board, self.previous_board):
                        print(MOVE_NOT_VALID)
                    elif ply.action == PROMOTE:
                        ply.promotion = self.promotion_input()
                        break
                    else:
                        break
                
                # Add the ply to the history
                self.add_ply(ply)
                
                # Print board
                print(self.board)

                # Checks
                is_check = Rules().is_check(self.board, opposite_color(color))
                if is_check:
                    print("Check!")
                
                # Finishing condition
                if Rules().is_finished(self.board, self.previous_board, opposite_color(color)):
                    self.is_finished = True
                    if is_check:
                        print(f"{color} won!")
                    else:
                        print("It's a draw!")
                    break


    def color_input(self) -> str:
        """
        Returns a chess color given by the player.
        """
        while True:
            color_input = input(PICK_COLOR_MSG)

            if color_input in BLACK_NAMES:
                return BLACK
            elif color_input in WHITE_NAMES:
                return WHITE
            else:
                print(PICK_COLOR_ERROR_MSG)


    def ply_input(self, color: str) -> Ply:
        """
        Returns a ply given by the player if the square selected is occupied by a piece
        of the given color.
        """
        while True:
            while True:
                start = square_to_index(input(f"{color.capitalize()} moves. Start square: "))
                if start:
                    start_row, start_col = start
                    piece = self.board.state[start_row - 1][start_col - 1]
                    if piece:
                        if piece.color == color:
                            break
                        else:
                            print(INVALID_COLOR_MSG)
                    else:
                        print(EMPTY_SQ_MSG)
                else:
                    print(INVALID_SQ)
            while True:
                finish = square_to_index(input("Finish square: "))
                if finish:
                    break
                else:
                    print(INVALID_SQ)
            return Ply().set_start(start).set_finish(finish).set_piece(piece)


    def promotion_input(self) -> str:
        """
        Inputs a piece type valid for pawn promotion.
        """
        while True:
            promotion_input = get_piece_name(input("Choose a piece to promote to: "))
            if promotion_input in [QUEEN, KNIGHT, BISHOP, TOWER]:
                return promotion_input
            else:
                print(INVALID_PROMOTION)
