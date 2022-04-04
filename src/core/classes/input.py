from string import ascii_lowercase
from src.core.classes.board_controller import BoardController
from src.config.constants import BISHOP_NAMES, BLACK_NAMES, EMPTY_SQ_MSG, INVALID_COLOR_MSG, INVALID_PROMOTION, INVALID_SQ, KING_NAMES, KNIGHT_NAMES, PAWN_NAMES, QUEEN_NAMES, TOWER_NAMES, WHITE_NAMES
from src.core.classes.color import Black, Color, White
from src.core.classes.piece import Bishop, King, Knight, Pawn, Queen, Rook
from src.core.classes.ply import Ply
from src.core.classes.position import Position, PositionError


class Input:
    @classmethod
    def color(self, text: str) -> Color:
        if text.upper() in BLACK_NAMES:
            return Black()
        elif text.upper() in WHITE_NAMES:
            return White()
        raise ValueError()

    @classmethod
    def position(self, text_input: str) -> Position:
        if len(text_input) == 2:
            col = text_input[0]
            row = text_input[1]
            if 'a' <= col <= 'h' and '1' <= row <= '8':
                return Position(ascii_lowercase.index(col), int(row) - 1)
        raise PositionError()

    @classmethod
    def ply(self, color: Color) -> Ply:
        """
        Returns a ply given by the player if the square selected is occupied by a piece
        of the given color.
        """
        while True:
            while True:
                try:
                    start = self.position_input(input(f"{str(color)} moves. Start square: "))
                except PositionError:
                    print(INVALID_SQ)
                except Exception as err:
                    raise err
                else:
                    piece = self.controller.board.get_piece(start)
                    if piece:
                        if piece.color == color:
                            break
                        else:
                            print(INVALID_COLOR_MSG)
                    else:
                        print(EMPTY_SQ_MSG)
            while True:
                try:
                    finish = self.position_input(input("Finish square: "))
                except PositionError:
                    print(INVALID_SQ)
                except Exception as err:
                    raise err
                else:
                    break

            return Ply(start,finish,piece)

    @classmethod
    def piece_class(name: str) -> type:
        """
        This function standardizes the chess piece names.
        """
        if name in PAWN_NAMES:
            return Pawn
        elif name in KNIGHT_NAMES:
            return Knight
        elif name in BISHOP_NAMES:
            return Bishop
        elif name in TOWER_NAMES:
            return Rook
        elif name in QUEEN_NAMES:
            return Queen
        elif name in KING_NAMES:
            return King
        else:
            return None

    @classmethod
    def promotion(self) -> type:
        """
        Inputs a piece type valid for pawn promotion.
        """
        while True:
            promotion_input = self.piece_class(input("Choose a piece to promote to: "))
            if promotion_input in [Queen, Knight, Bishop, Rook]:
                return promotion_input
            else:
                print(INVALID_PROMOTION)

