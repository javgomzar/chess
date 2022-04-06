from numpy import isin
from src.core.classes.actions import EnPassant, LeftCastle, RightCastle, Move, Promote
from src.core.classes.board_controller import BoardController
from src.core.error_classes.errors import PositionError
from src.config.constants import LEFT, RIGHT
from src.core.classes.board import Board
from src.core.classes.color import Black, Color
from src.core.classes.piece import Piece
from src.core.classes.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from src.core.classes.ply import Ply
from src.core.classes.position import Position, Vector
from src.core.metaclasses.Singleton import Singleton


class Rules(metaclass=Singleton):
    """
    Class with all the methods relevant for chess rules. 
    """
    def set_action(self, ply: Ply, controller: BoardController) -> None:
        if isinstance(ply.piece, Pawn):
            if ply.to_position.row == ply.piece.color.opposite_color().king_row:
                ply.action = Promote(ply.piece)
                return
            previous_board = controller.get_previous_board()
            previous_pawn = previous_board.get_piece(Position(ply.to_position.col, ply.color.opposite_color().pawn_row))
            taken_pawn = controller.board.get_piece(ply.to_position + (-ply.piece.color.pawn_direction))
            if self.en_passant(previous_pawn, taken_pawn, ply):
                ply.action = EnPassant(ply.piece, ply.to_position)
                return
        elif isinstance(ply.piece, King):
            if ply.piece.is_left_castle(ply.to_position):
                rook = controller.board.get_piece(Position(0, ply.color.king_row))
                action_class = LeftCastle
            elif ply.piece.is_right_castle(ply.to_position):
                rook = controller.board.get_piece(Position(7, ply.color.king_row))
                action_class = RightCastle
            else:
                rook = None
            if rook and isinstance(rook, Rook) and not rook.has_moved:
                ply.action = action_class(ply.color)
                return
        ply.action = Move(ply.piece, ply.to_position)
        return

    def validate(self, ply: Ply, controller: BoardController) -> bool:
        """
        Validates a ply for the current board and a previous board. Returns `True` if the ply is valid
        and `False` if it's not valid. If the ply is valid, this method fills the action attribute for
        the ply.
        """
        if not ply.piece.can_move(ply.to_position):
            return False
        
        self.set_action(ply, controller)
        current_board = controller.board.copy()
        piece_taken = current_board.get_piece(ply.to_position)

        # Can't take your own piece or move if the piece is pinned
        if self.is_pinned(ply, controller) or piece_taken and piece_taken.color == ply.color:
            return False

        # Blocks
        elif not isinstance(ply.piece, Knight) and self.is_blocked(ply, current_board):
            return False

        # Pawns are special
        elif isinstance(ply.piece, Pawn):
            piece_taken = current_board.get_piece(ply.to_position)

            #Pawn diagonal moves
            if piece_taken:
                if (isinstance(ply.action, Move) or isinstance(ply.action, Promote)) and \
                    ply.piece.is_capture(ply.to_position):
                    return True
                else:
                    return False
            elif isinstance(ply.action, EnPassant) or not ply.piece.is_capture(ply.to_position):
                return True
            else:
                return False           

        # Can't castle if there is a check in the way
        if isinstance(ply.action, LeftCastle) or isinstance(ply.action, RightCastle):
            for n in range(0,3):
                if self.is_check(possible_board, ply.color):
                    break
                pointer += direction
                possible_board = current_board.copy().move_piece(ply.from_position, pointer)
        else:
            return True

    def en_passant(self, previous_pawn: Pawn, taken_pawn: Pawn, ply: Ply) -> bool:
        """
        Checks if a ply is an "en passant" move.
        """
        return previous_pawn and taken_pawn and \
               isinstance(previous_pawn, Pawn) and \
               isinstance(taken_pawn, Pawn) and \
               not previous_pawn.has_moved and \
               ply.piece.is_capture(ply.to_position) and \
               ply.piece.position.row == (3 if ply.color == Black() else 4)

    def is_pinned(self, ply: Ply, controller: BoardController) -> bool:
        """
        Checks if a piece is pinned. This means that moving it 
        would leave the king in check.
        """
        controller.execute(ply.action)
        result = self.is_check(ply.color, controller.board)
        controller.roll_back()
        return result

    def is_blocked(self, ply: Ply, board: Board) -> bool:
        """
        Checks if a ply is a movement blocked by other piece.
        """
        delta = ply.to_position - ply.from_position
        norm = max(abs(delta.col), abs(delta.row))
        direction = Vector(int(delta.col / norm), int(delta.row / norm))
        pointer = ply.from_position + direction
        while pointer != ply.to_position:
            if board.get_piece(pointer):
                return True
            pointer = pointer + direction
        return False

    def is_check(self, color: Color, board: Board) -> bool:
        """
        Checks if a board contains a check for the king of a given color.
        """
        king_position = board.get_king(color).position

        # Knight checks... and king checks?
        for piece_class in [Knight, King]:
            for vector in piece_class.move_vectors:
                try:
                    pointer = king_position + vector
                except PositionError:
                    pass
                else:
                    piece = board.get_piece(pointer)
                    if piece and isinstance(piece, piece_class) and piece.color != color:
                        return True
        
        # Bishop and rook checks (and Queen)
        for piece_class in [Bishop, Rook]:
            for direction in piece_class.move_directions:
                try:
                    pointer = king_position + direction
                except PositionError:
                    break
                piece = board.get_piece(pointer)
                if piece:
                    if piece.color == color:
                        break
                    elif isinstance(piece,piece_class) or isinstance(piece,Queen):
                        return True
                    else:
                        break

        # Pawn checks
        for direction in [color.pawn_direction + Vector(delta_col, 0) for delta_col in [-1,1]]:
            try:
                pointer = king_position + direction
            except PositionError:
                break
            piece = board.get_piece(pointer)
            if piece and isinstance(piece, Pawn) and piece.color != color:
                return True

        return False

    def get_valid_moves(self, piece: Piece, controller: BoardController) -> list[tuple]:
        """
        Returns all valid moves for the piece in a given position.
        """        
        result = []
        for possible_move in piece.available_positions():
            if self.validate(Ply(piece.position, possible_move, piece),controller):
                result.append(possible_move)
        return result


    def is_finished(self, color: Color, controller: BoardController) -> bool:
        for piece in controller.board.get_pieces(color=color, is_active=True):
            valid_moves = self.get_valid_moves(piece, controller)
            if valid_moves:
                return False
        else:
            return True            
