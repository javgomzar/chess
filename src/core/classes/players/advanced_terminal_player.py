import re
from ..error_classes.errors import InvalidInput
from ..board import Board
from .terminal_player import TerminalPlayer
from ..error_classes import AmbiguousMove
from ..ply import Ply
from ..position import Position
from ..pieces import Pawn
from string import ascii_lowercase


class AdvancedTerminalPlayer(TerminalPlayer):
    def input_promotion(self, board: Board) -> type:
        return self.to_piece_class

    def input_ply(self, board: Board) -> Ply:
        while True:
            try:
                notation = input(f"{str(self.color)} moves. Select move in algebraic notation: ")
                ply = self.ply_from_notation(notation, board)
            except AmbiguousMove:
                print("Ambiguous move.")
            except InvalidInput:
                print("Invalid input.")
            except Exception as err:
                raise err
            else:
                break
        return ply

    def ply_from_notation(self, notation: str, board: Board) -> Ply:
        general_regex = r"([BKNQR]?)([a-h]?)([1-8]?)(x?)([a-h][1-8])([BNQR]?)"
        short_castle_regex = r"(O-O|0-0)"
        long_castle_regex = r"(O-O-O|0-0-0)"

        match = re.search(general_regex, notation)
        if not match:
            short_castle_match = re.search(short_castle_regex, notation)
            king_row = self.color.king_row
            if short_castle_match:
                return Ply(self.color, Position(4, king_row), Position(6, king_row))
            long_castle_match = re.search(long_castle_regex, notation)
            if long_castle_match:
                return Ply(self.color, Position(4, king_row), Position(2, king_row))
            raise InvalidInput()

        non_pawn_symbol = match.group(1)
        piece_type = self.input_piece_class(non_pawn_symbol) if non_pawn_symbol else Pawn

        is_capture = bool(match.group(4))

        to_position = Position.from_notation(match.group(5))
        from_position = None

        self.to_piece_class = self.input_piece_class(match.group(6))

        disambiguation_col = match.group(2)
        disambiguation_row = match.group(3)
        if disambiguation_col and disambiguation_row:
            from_position = Position.from_notation(disambiguation_col + disambiguation_row)
            return Ply(self.color, from_position, to_position)

        possible_pieces = board.get_pieces(self.color, is_active=True, piece_type=piece_type)
        possible_pieces = [piece for piece in possible_pieces if piece.can_move(to_position - board.get_position(piece))]

        if disambiguation_col:
            disambiguation_col = ascii_lowercase[0:8].index(disambiguation_col)
            possible_pieces = [piece for piece in possible_pieces if board.get_position(piece).col == disambiguation_col]
        if disambiguation_row:
            disambiguation_row = int(disambiguation_col) - 1
            possible_pieces = [piece for piece in possible_pieces if board.get_position(piece).row == disambiguation_row]

        if len(possible_pieces) > 1:
            if piece_type == Pawn:
                possible_pieces = [piece for piece in possible_pieces if is_capture == piece.is_capture(to_position - board.get_position(piece))]
            else:
                raise AmbiguousMove()
        if len(possible_pieces) == 1:
            piece = possible_pieces[0]
            return Ply(self.color, board.get_position(piece), to_position)
        if len(possible_pieces) == 0:
            raise InvalidInput()
        raise Exception()
