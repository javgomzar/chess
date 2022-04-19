from abc import ABC, abstractmethod
from src.core.classes.pieces.bishop import Bishop
from src.core.classes.pieces.king import King
from src.core.classes.pieces.knight import Knight
from src.core.classes.pieces.pawn import Pawn
from src.core.classes.pieces.piece import Piece
from src.core.classes.pieces.queen import Queen
from src.core.classes.pieces.rook import Rook
from src.core.classes.position import Vector
from src.core.error_classes.errors import PositionError
from src.core.classes.color import Color
from src.core.classes.ply import Ply
from src.core.classes.board import Board
from src.core.classes.board_controller import BoardController


class GameMode(ABC):
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

    def get_valid_moves(self, piece: Piece, controller: BoardController) -> list[tuple]:
        """
        Returns all valid moves for the piece in a given position.
        """        
        result = []
        from_position = controller.board.get_position(piece)
        for possible_move in piece.available_positions(from_position):
            if self.validate(Ply(piece.color, from_position, possible_move), controller):
                result.append(possible_move)
        return result
    
    def is_finished(self, color: Color, controller: BoardController) -> bool:
        for piece in controller.board.get_pieces(color=color, is_active=True):
            if len(self.get_valid_moves(piece, controller)) > 0:
                return False
        else:
            return True

    @abstractmethod
    def init_board(self) -> Board:
        pass

    @abstractmethod
    def validate(self, ply: Ply, controller: BoardController) -> bool:
        pass
    
    @abstractmethod
    def is_win(self, color: Color, controller: BoardController) -> bool:
        pass
