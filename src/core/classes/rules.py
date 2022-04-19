from src.core.classes.actions.action import Action
from src.core.classes.actions import Castle, EnPassant, Move, Promote
from src.core.classes.board_controller import BoardController
from src.core.error_classes.errors import PositionError
from src.core.classes.board import Board
from src.core.classes.color import Black, Color
from src.core.classes.pieces.piece import Piece
from src.core.classes.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from src.core.classes.ply import Ply
from src.core.classes.position import Position, Vector
from src.core.abstract_classes.singleton import Singleton


class Rules(metaclass=Singleton):
    """
    Class with all the methods relevant for chess rules. 
    """
    def set_action(self, ply: Ply, controller: BoardController) -> None:
        if isinstance(ply.piece, Pawn):
            if ply.to_position.row == ply.piece.color.opposite_color().king_row:
                ply.action = Promote(ply.piece, ply.vector)
                return
            if self.en_passant(ply, controller):
                ply.action = EnPassant(ply.piece, ply.to_position)
                return
        elif isinstance(ply.piece, King):
            if ply.piece.is_castle(ply.to_position):
                is_left_castle = ply.piece.is_left_castle(ply.vector)
                rook_col,direction = (0, Vector(-1,0)) if is_left_castle else (7, Vector(1,0))
                rook = controller.board.get_piece(Position(rook_col, ply.color.king_row))
                if rook and isinstance(rook, Rook) and not rook.has_moved:
                    ply.action = Castle(ply.color, direction)
                    return
        ply.action = Move(ply.piece, ply.vector)
        return

    def validate(self, ply: Ply, controller: BoardController) -> Action:
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

    def is_pinned(self, ply: Ply, controller: BoardController) -> bool:
        """
        Checks if a piece is pinned. This means that moving it 
        would leave the king in check.
        """
        possible_board = controller.try_action(ply.action)
        return self.is_check(ply.color, possible_board)

    def is_blocked(self, ply: Ply, board: Board) -> bool:
        """
        Checks if a ply is a movement blocked by other piece.
        """
        direction = ply.vector.normalize()
        pointer = ply.from_position + direction
        while pointer != ply.to_position:
            if board.get_piece(pointer):
                return True
            pointer += direction
        return False

    def is_check(self, color: Color, board: Board) -> bool:
        """
        Checks if a board contains a check for the king of a given color.
        """
        king_position = board.get_king_position(color)

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
                pointer = king_position
                while True:
                    try:
                        pointer += direction
                    except PositionError:
                        break
                    else:
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
        from_position = controller.board.get_position(piece)
        for possible_move in piece.available_positions(from_position):
            if self.validate(Ply(from_position, possible_move, piece), controller):
                result.append(possible_move)
        return result


    def is_finished(self, color: Color, controller: BoardController) -> bool:
        for piece in controller.board.get_pieces(color=color, is_active=True):
            valid_moves = self.get_valid_moves(piece, controller)
            if valid_moves:
                return False
        else:
            return True            
