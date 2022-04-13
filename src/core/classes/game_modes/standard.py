from src.core.classes.actions.castle import Castle
from src.core.classes.actions.move import Move
from src.core.classes.actions.en_passant import EnPassant
from src.core.classes.actions.promote import Promote
from src.core.classes.board_controller import BoardController
from src.core.classes.actions.action import Action
from src.core.classes.ply import Ply
from src.core.classes.position import Position, Vector
from src.core.classes.pieces import Bishop, Knight, King, Pawn, Queen, Rook
from src.core.classes.color import Black, White
from src.core.classes.board import Board


class Standard:
    def init_board(self) -> Board:
        board = Board()
        for color in [Black(), White()]:
                for col,class_pair in enumerate(zip([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook], [Pawn]*8)):
                    for row,piece_class in zip((color.king_row, color.pawn_row), class_pair):
                        board.add(piece_class(color), Position(col,row))
        return board

    def get_action(self, ply: Ply, controller: BoardController) -> Action:
        piece = controller.board.get_piece(ply.from_position)
        vector = ply.to_position - ply.from_position

        if isinstance(piece, Pawn):
            if ply.to_position.row == ply.color.opposite_color().king_row:
                return Promote(piece, vector)
            if self.en_passant(ply, controller):
                return EnPassant(piece, ply.to_position)
        elif isinstance(piece, King):
            if piece.is_castle(ply.to_position):
                is_left_castle = piece.is_left_castle(vector)
                rook_col,direction = (0, Vector(-1,0)) if is_left_castle else (7, Vector(1,0))
                rook = controller.board.get_piece(Position(rook_col, ply.color.king_row))
                if rook and isinstance(rook, Rook) and not rook.has_moved:
                    return Castle(ply.color, direction)
        return Move(piece, vector)

    def validate(self, action: Action, controller: BoardController) -> bool:
        """
        Validates a ply for the current board and a previous board. Returns `True` if the ply is valid
        and `False` if it's not valid. If the ply is valid, this method fills the action attribute for
        the ply.
        """
        if not ply.piece.can_move(ply.vector):
            return False
        
        self.set_action(ply, controller)
        current_board = controller.board.copy()
        piece_taken = current_board.get_piece(ply.to_position)

        # Exclude taking your own piece, pins and blocks
        if piece_taken and piece_taken.color == ply.color or \
           not isinstance(ply.piece, Knight) and self.is_blocked(ply, current_board) or \
           self.is_pinned(ply, controller):
            return False

        # Pawns can only move diagonally under certain conditions
        elif isinstance(ply.piece, Pawn):
            if piece_taken:
                if (isinstance(ply.action, Move) or isinstance(ply.action, Promote)) and \
                    ply.piece.is_capture(ply.to_position - ply.from_position):
                    return True
                else:
                    return False
            elif isinstance(ply.action, EnPassant) or not ply.piece.is_capture(ply.to_position - ply.from_position):
                return True
            else:
                return False           

        # Can't castle if there is a check in the way
        if isinstance(ply.action, Castle):
            pointer = ply.color.king_position
            direction = ply.action.direction
            for n in range(0,2):
                pointer += direction
                possible_board = controller.try_action(Move(ply.piece, direction))
                if self.is_check(ply.color, possible_board):
                    return False
        return True
    