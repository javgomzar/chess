from string import ascii_lowercase
import re

from ..error_classes import AmbiguousMove
from ..pieces import piece_class_from_text, Pawn, Rook
from ..board import Board
from ..color import Color
from ..error_classes import InvalidInput
from ..position import Position
from ..rules import Block

from .ply import Ply


def ply_from_notation(color: Color, notation: str, board: Board) -> Ply:
        general_regex = r"([BKNQR]?)([a-h]?)([1-8]?)(x?)([a-h][1-8])([BNQR]?)"
        short_castle_regex = r"(O-O|0-0)"
        long_castle_regex = r"(O-O-O|0-0-0)"

        match = re.search(general_regex, notation)
        if not match:
            short_castle_match = re.search(short_castle_regex, notation)
            king_row = color.king_row
            if short_castle_match:
                return Ply(color, Position(4, king_row), Position(6, king_row))
            long_castle_match = re.search(long_castle_regex, notation)
            if long_castle_match:
                return Ply(color, Position(4, king_row), Position(2, king_row))
            raise InvalidInput()

        non_pawn_symbol = match.group(1)
        piece_type = piece_class_from_text(non_pawn_symbol) if non_pawn_symbol else Pawn

        is_capture = bool(match.group(4))

        to_position = Position.from_notation(match.group(5))
        from_position = None

        disambiguation_col = match.group(2)
        disambiguation_row = match.group(3)
        if disambiguation_col and disambiguation_row:
            from_position = Position.from_notation(disambiguation_col + disambiguation_row)
            return Ply(color, from_position, to_position)

        possible_pieces = board.get_pieces(color, is_active=True, piece_type=piece_type)
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
            elif piece_type == Rook:
                possible_pieces = [piece for piece in possible_pieces if Block.validate(Ply(color, board.get_position(piece), to_position), board)]
            else:
                raise AmbiguousMove()
        if len(possible_pieces) == 1:
            piece = possible_pieces[0]
            return Ply(color, board.get_position(piece), to_position)
        if len(possible_pieces) == 0:
            raise InvalidInput()
        raise Exception()
