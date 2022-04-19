from src.core.classes.game_modes.game_mode import GameMode
from src.core.classes.actions.castle import Castle
from src.core.classes.actions.move import Move
from src.core.classes.actions.en_passant import EnPassant
from src.core.classes.actions.promote import Promote
from src.core.classes.board_controller import BoardController
from src.core.classes.actions.action import Action
from src.core.classes.ply import Ply
from src.core.classes.position import Position, Vector
from src.core.classes.pieces import Bishop, Knight, King, Pawn, Queen, Rook
from src.core.classes.color import Black, Color, White
from src.core.classes.board import Board


class Standard(GameMode):
    def get_action(self, ply: Ply, controller: BoardController) -> Action:
        piece = controller.board.get_piece(ply.from_position)
        vector = ply.to_position - ply.from_position

        if isinstance(piece, Pawn):
            if ply.to_position.row == ply.color.opposite_color().king_row:
                return Promote(piece, vector)
            if self.en_passant(ply, controller):
                return EnPassant(piece, ply.to_position)
        elif isinstance(piece, King):
            if piece.is_castle(ply.vector):
                is_left_castle = piece.is_left_castle(vector)
                rook_col,direction = (0, Vector(-1,0)) if is_left_castle else (7, Vector(1,0))
                rook = controller.board.get_piece(Position(rook_col, ply.color.king_row))
                if rook and isinstance(rook, Rook) and not rook.has_moved:
                    return Castle(ply.color, direction)
        return Move(piece, vector)

    def en_passant(self, ply: Ply, controller: BoardController) -> bool:
        """
        Checks if a ply is an "en passant" move.
        """
        taken_piece = controller.board.get_piece(ply.to_position)
        if Pawn(ply.color, has_moved=True).is_capture(ply.vector) and not taken_piece:
            passed_pawn_position = ply.to_position + (-ply.color.pawn_direction)
            passed_pawn = controller.board.get_piece(passed_pawn_position)
            previous_board = controller.get_previous_board()
            previous_pawn_position = Position(ply.to_position.col, ply.color.opposite_color().pawn_row)
            previous_pawn = previous_board.get_piece(previous_pawn_position)
            return previous_pawn and passed_pawn and \
                   previous_pawn.id == passed_pawn.id and \
                   ply.from_position.row == (3 if ply.color == Black() else 4)

    def init_board(self) -> Board:
        board = Board()
        for color in [Black(), White()]:
                for col,class_pair in enumerate(zip([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook], [Pawn]*8)):
                    for row,piece_class in zip((color.king_row, color.pawn_row), class_pair):
                        board.add(piece_class(color), Position(col,row))
        return board

    def validate(self, ply: Ply, controller: BoardController) -> bool:
        """
        Validates a ply for the current board and a previous board. Returns `True` if the ply is valid
        and `False` if it's not valid. If the ply is valid, this method fills the action attribute for
        the ply.
        """
        piece = controller.board.get_piece(ply.from_position)

        if not piece.can_move(ply.vector):
            return False
        
        ply.action = self.get_action(ply, controller)

        current_board = controller.board.copy()
        piece_taken = current_board.get_piece(ply.to_position)

        # Exclude taking your own piece, pins and blocks
        if piece_taken and piece_taken.color == ply.color or \
           not isinstance(piece, Knight) and self.is_blocked(ply, current_board) or \
           self.is_pinned(ply, controller):
            return False

        # Pawns can only move diagonally under certain conditions
        elif isinstance(piece, Pawn):
            if piece_taken:
                if (isinstance(ply.action, Move) or isinstance(ply.action, Promote)) and \
                    piece.is_capture(ply.to_position - ply.from_position):
                    return True
                else:
                    return False
            elif isinstance(ply.action, EnPassant) or not piece.is_capture(ply.to_position - ply.from_position):
                return True
            else:
                return False           

        # Can't castle if there is a check in the way
        if isinstance(ply.action, Castle):
            pointer = ply.color.king_position
            direction = ply.action.direction
            for n in range(0,2):
                pointer += direction
                possible_board = controller.try_action(Move(piece, direction))
                if self.is_check(ply.color, possible_board):
                    return False
        return True

    def is_win(self, color: Color, controller: BoardController):
        self.is_check(color.opposite_color(), controller.board)
