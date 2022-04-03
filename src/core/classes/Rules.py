from core.classes.actions import FirstMove, Remove
from src.core.classes.board_controller import BoardController
from src.core.error_classes.errors import PositionError
from src.config.constants import LEFT, RIGHT, PAWN
from src.core.classes.actions import Move, Promote
from src.core.classes.board import Board
from src.core.classes.color import Black, Color
from src.core.classes.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from src.core.classes.ply import Ply
from src.core.classes.position import Position, Vector
from src.core.metaclasses.Singleton import Singleton
from src.core.utils import sum_tuple
import copy


class Rules(metaclass=Singleton):
    """
    Class with all the methods relevant for chess rules. 
    """
    def __init__(self) -> None:
        pass

    def set_action(self, ply: Ply, controller: BoardController) -> None:
        if not ply.piece.has_moved:
            ply.action = FirstMove(ply.piece, ply.to_position)
        

    def validate(self, ply: Ply, controller: BoardController) -> bool:
        """
        Validates a ply for the current board and a previous board. Returns `True` if the ply is valid
        and `False` if it's not valid. If the ply is valid, this method fills the action attribute for
        the ply.
        """
        if not ply.piece.can_move(ply.start, ply.finish):
            return False
        
        current_board = controller.board.copy()
        previous_board = controller.get_previous_board()
        piece_taken = current_board.get_piece(ply.finish)

        # Can't take your own piece or move if the piece is pinned
        if piece_taken.color == ply.color or self.is_pinned(ply, current_board):
            return False

        # Blocks
        elif not isinstance(ply.piece, Knight) and self.is_blocked(ply, current_board):
            return False

        # Pawns are special
        elif isinstance(ply.piece, Pawn):
            piece_taken = current_board.state[ply.finish]

            #Pawn diagonal moves
            if ply.piece.is_capture(ply.start, ply.finish):
                if piece_taken:
                    ply.set_action(Move)
                    result = True
                elif self.en_passant(ply, current_board, previous_board):
                    ply.set_action(EnPassant)
                    result = True
                else:
                    result = False

            # Pawn advancements
            elif ply.piece.can_move(ply.start, ply.finish) and not piece_taken:
                ply.set_action(Move)
                result = True
            else:
                result = False

            # Pawn promotions
            if result:
                if ply.finish.row == ply.color.opposite_color().king_row_index:
                    ply.set_action(Promote)
            
            return result

        # Kings are also special
        elif isinstance(ply.piece, King):
            if ply.piece.can_move(ply.start,ply.finish):
                ply.set_action(Move)
                return True
            
            # Castling
            elif not current_board.king_moved[ply.color]:
                delta = ply.finish - ply.start
                side,direction = (RIGHT, Vector(1,0)) if delta.col > 0 else (LEFT, Vector(-1,0))
                if delta.row == 0 and abs(delta.col) == 2 and not current_board.rook_moved[ply.color][side]:
                    pointer = ply.start
                    possible_board = current_board.copy()

                    # Can't castle if there is a check in the way
                    for n in range(0,3):
                        if self.is_check(possible_board, ply.color):
                            break
                        pointer += direction
                        possible_board = current_board.copy().move_piece(ply.start, pointer)
                    else:
                        ply.set_action(Castle)
                        return True
                    return False
                else:
                    return False
            else:
                return False
        elif ply.piece.can_move(ply.start, ply.finish):
            ply.set_action(Move)
            return True
        else:
            return False
    
    def is_same_color(self, ply: Ply, board: Board) -> bool:
        """
        Checks if the ply is moving a piece to a square occupied by a piece 
        of the same color.
        """
        finish_piece = board.state[ply.finish]
        return finish_piece and finish_piece.color == ply.color

    def en_passant(self, ply: Ply, current_board: Board, previous_board: Board) -> bool:
        """
        Checks if a ply is an "en passant" move.
        """
        start_row = ply.start.row
        valid_start_row, valid_finish_row, current_row, previous_row = (4,3,3,1) if ply.color == Black() else (5,6,4,6)
        if start_row == valid_start_row and ply.finish.row == valid_finish_row:
            current_pawn = current_board.state[current_row][ply.finish.col-1]
            previous_pawn = previous_board.state[previous_row][ply.finish.col-1]
            if current_pawn and previous_pawn \
            and current_pawn.name  == PAWN \
            and current_pawn.color != ply.color \
            and current_pawn.id == previous_pawn.id:
                return True
        return False

    def is_pinned(self, ply: Ply, board: Board) -> bool:
        """
        Checks if a piece is pinned. This means that moving it 
        would leave the king in check.
        """
        controller = BoardController(board)
        piece_taken = board.get_piece(ply.finish)
        if piece_taken:
            controller.execute(Remove(piece_taken))
        controller.execute(Move(ply.piece, to_position=ply.finish))
        result = self.is_check(board, ply.color)
        controller.undo()
        return result

    def is_blocked(self, ply: Ply, board: Board) -> bool:
        """
        Checks if a ply is a movement blocked by other piece.
        """
        if ply.piece in [Pawn, Bishop, Rook, Queen]:
            
        
            delta = ply.finish - ply.start
            norm = max(abs(delta.col), abs(delta.row))
            direction = Vector(int(delta.col / norm), int(delta.row / norm))
            pointer = ply.start + direction
            while pointer != ply.finish:
                if board.state[pointer]:
                    return True
                pointer = pointer + direction
        else:
            return False

    def is_check(self, color: Color, controller: BoardController) -> bool:
        """
        Checks if a board contains a check for the king of a given color.
        """
        king_position = controller.board.get_king_position(color)

        # Knight checks... and king checks?
        for piece_class in [Knight, King]:
            for vector in piece_class.move_vectors:
                try:
                    pointer = king_position + vector
                except PositionError:
                    pass
                else:
                    piece = controller.board.get_piece(pointer)
                    if piece and isinstance(piece, piece_class) and piece.color != color:
                        return True
        
        # Bishop and rook checks (and Queen)
        for piece_class in [Bishop, Rook]:
            for direction in piece_class.move_directions:
                try:
                    pointer = king_position + direction
                except PositionError:
                    break
                piece = controller.board.get_piece(pointer)
                if piece:
                    if piece.color == color:
                        break
                    elif isinstance(piece,piece_class) or isinstance(piece,Queen):
                        return True
                    else:
                        break

        # Pawn checks
        for direction in [Vector(delta_col, color.pawn_row_delta) for delta_col in [-1,1]]:
            try:
                pointer = king_position + direction
            except PositionError:
                break
            piece = controller.board.get_piece(pointer)
            if piece and isinstance(piece, Pawn) and piece.color != color:
                return True

        return False

    def get_valid_moves(self, position: Position, current_board: Board, previous_board: Board) -> list[tuple]:
        """
        Returns all valid moves for the piece in a given position.
        """        
        piece = current_board.state[position]
        result = []
        if piece:
            for possible_move in piece.available_positions(position):
                if self.validate(Ply(position, possible_move, piece),
                                     current_board, previous_board):
                    result.append(possible_move)
        return result


    def is_finished(self, current_board: Board, previous_board: Board, color: str) -> bool:
        for position in current_board.active_pieces[color].keys():
            valid_moves = self.get_valid_moves(position, current_board, previous_board)
            if valid_moves:
                return False
        else:
            return True            
