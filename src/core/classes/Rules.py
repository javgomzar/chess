from src.config.constants import BLACK, CASTLE, EN_PASSANT, MOVE, PROMOTE, WHITE, LEFT, RIGHT, DIRECTIONS, KNIGHT_MOVES, PAWN, BISHOP, KNIGHT, TOWER, KING,  QUEEN
from src.core.classes.Board import Board
from src.core.classes.Piece import Piece
from src.core.classes.Ply import Ply
from src.core.utils import is_valid_position, sum_tuple
import copy

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Rules(metaclass=Singleton):
    """
    Class with all the methods relevant for chess rules. 
    """
    def __init__(self) -> None:
        self.valid_moves_dict = {
            QUEEN: self.is_queen_move,
            TOWER: self.is_tower_move,
            BISHOP: self.is_bishop_move,
            KNIGHT: self.is_knight_move
        }

    def validate(self, ply: Ply, current_board: Board, previous_board: Board) -> bool:
        """
        Validates a ply for the current board and a previous board. Returns `True` if the ply is valid
        and `False` if it's not valid. If the ply is valid, this method fills the action attribute for
        the ply.
        """

        # Can't take your own piece or move if the piece is pinned
        if self.is_same_color(ply, current_board) or self.is_pinned(ply, current_board):
            return False

        # Blocks
        elif ply.piece.name != KNIGHT and self.is_blocked(ply, current_board):
            return False

        # Pawns are special
        elif ply.piece.name == PAWN:
            finish_row, finish_col = ply.finish
            piece_taken = current_board.state[finish_row-1][finish_col-1]

            #Pawn diagonal moves
            if self.is_pawn_capture(ply):
                if piece_taken:
                    ply.set_action(MOVE)
                    result = True
                elif self.en_passant(ply, current_board, previous_board):
                    ply.set_action(EN_PASSANT)
                    result = True
                else:
                    result = False

            # Pawn advancements
            elif self.is_pawn_move(ply) and not piece_taken:
                ply.set_action(MOVE)
                result = True
            else:
                result = False

            # Pawn promotions
            if result:
                if ply.color == BLACK and ply.finish[0] == 1 or \
                   ply.color == WHITE and ply.finish[0] == 8:
                    ply.set_action(PROMOTE)
            
            return result

        # Kings are also special
        elif ply.piece.name == KING:
            if self.is_king_move(ply):
                ply.set_action(MOVE)
                return True
            
            # Castling
            elif not current_board.king_moved[ply.color]:
                Dy = ply.finish[1] - ply.start[1]
                Dx = ply.finish[0] - ply.start[0]
                side,direction = (RIGHT, (0,1)) if Dy > 0 else (LEFT, (0,-1))
                if Dx == 0 and abs(Dy) == 2 and not current_board.tower_moved[ply.color][side]:
                    pointer = ply.start
                    possible_board = current_board

                    # Can't castle if there is a check in the way
                    for n in range(0,3):
                        if self.is_check(possible_board, ply.color):
                            break
                        pointer = sum_tuple(pointer, direction)
                        possible_board = copy.deepcopy(current_board).move_piece(ply.start, pointer)
                    else:
                        ply.set_action(CASTLE)
                        return True
                    return False
                else:
                    return False
            else:
                return False
        elif self.valid_moves_dict[ply.piece.name](ply):
            ply.set_action(MOVE)
            return True
        else:
            return False
    
    def is_same_color(self, ply: Ply, board: Board) -> bool:
        """
        Checks if the ply is moving a piece to a square occupied by a piece 
        of the same color.
        """
        finish_row, finish_col = ply.finish
        finish_piece = board.state[finish_row-1][finish_col-1]
        return finish_piece and finish_piece.color == ply.color
    
    def is_king_move(self, ply: Ply) -> bool:
        """
        Checks if a ply is a standard king move (excluding castling).
        """
        Dx = abs(ply.finish[0] - ply.start[0])
        Dy = abs(ply.finish[1] - ply.start[1])
        return True if max(Dx,Dy) == 1 else False

    def is_bishop_move(self, ply: Ply) -> bool:
        """
        Checks if a ply is a valid bishop move.
        """
        Dx = ply.finish[0] - ply.start[0]
        Dy = ply.finish[1] - ply.start[1]
        return True if Dy == Dx or Dy == -Dx else False

    def is_tower_move(self, ply: Ply) -> bool:
        """
        Checks if a ply is a valid tower move.
        """
        Dx = ply.finish[0] - ply.start[0]
        Dy = ply.finish[1] - ply.start[1]
        return True if Dy == 0 or Dx == 0 else False

    def is_queen_move(self, ply: Ply) -> bool:
        """
        Checks if a ply is a valid queen move.
        """
        return self.is_bishop_move(ply) or self.is_tower_move(ply)

    def is_knight_move(self, ply: Ply) -> bool:
        """
        Checks if a ply is a valid knight move.
        """
        Dx = abs(ply.finish[0] - ply.start[0])
        Dy = abs(ply.finish[1] - ply.start[1])
        return True if Dx + Dy == 3 and Dx != 0 and Dy != 0 else False 

    def is_pawn_move(self, ply: Ply) -> bool:
        """
        Checks if a ply is a pawn move, excluding captures.
        """
        Dx = ply.finish[0] - ply.start[0]
        Dy = ply.finish[1] - ply.start[1]
        is_black = ply.color == BLACK
        if Dy == 0:
            if is_black:
                return Dx == -1 or (Dx == -2 and ply.start[0] == 7)
            else:
                return Dx == 1 or (Dx == 2 and ply.start[0] == 2)
        else:
            return False

    def is_pawn_capture(self, ply: Ply) -> bool:
        """
        Checks if a ply is a capturing pawn move.
        """
        Dx = ply.finish[0] - ply.start[0]
        Dy = ply.finish[1] - ply.start[1]
        is_black = ply.color == BLACK
        if abs(Dy) == 1:
            return Dx == -1 if is_black else Dx == 1
        else:
            return False

    def en_passant(self, ply: Ply, current_board: Board, previous_board: Board) -> bool:
        """
        Checks if a ply is an "en passant" move.
        """
        finish_row, finish_col = ply.finish
        start_row = ply.start[0]
        valid_start_row, valid_finish_row, current_row, previous_row = (4,3,3,1) if ply.color == BLACK else (5,6,4,6)
        if start_row == valid_start_row and finish_row == valid_finish_row:
            current_pawn = current_board.state[current_row][finish_col-1]
            previous_pawn = previous_board.state[previous_row][finish_col-1]
            if current_pawn and previous_pawn \
            and current_pawn.name  == PAWN \
            and current_pawn.color != ply.color \
            and current_pawn.id == previous_pawn.id:
                return True
        return False

    def is_pinned(self, ply: Ply, board: Board) -> bool:
        """
        Checks if a ply is a pinned movement. This means that if executed, the move
        would leave the king in check.
        """
        possible_board = copy.deepcopy(board).move_piece(ply.start, ply.finish)
        return self.is_check(possible_board, ply.color)

    def is_blocked(self, ply: Ply, board: Board) -> bool:
        """
        Checks if a ply is a movement blocked by other piece.
        """
        Dx = ply.finish[0] - ply.start[0]
        Dy = ply.finish[1] - ply.start[1]

        # The movement has to be a straight line
        if Dx == 0 or Dy == 0 or Dy == Dx or Dy == -Dx:
            norm = max(abs(Dx), abs(Dy))
            direction = (int(Dx / norm), int(Dy / norm))
            pointer = sum_tuple(ply.start, direction)
            while pointer != ply.finish:
                if board.state[pointer[0]-1][pointer[1]-1]:
                    return True
                pointer = sum_tuple(pointer, direction)
        return False

    def is_check(self, board: Board, color: str) -> bool:
        """
        Checks if a board contains a check for the king of a given color.
        """
        king_position = board.king_position[color]

        # Knight checks
        for direction in KNIGHT_MOVES:
            row,col = sum_tuple(king_position, direction)
            if is_valid_position((row,col)):
                piece = board.state[row-1][col-1]
                if piece and piece.name == KNIGHT and piece.color != color:
                    return True
        
        # Bishop and tower checks
        for name in [BISHOP, TOWER]:
            for direction in DIRECTIONS[name]:
                pointer = sum_tuple(king_position, direction)
                while is_valid_position(pointer):
                    row,col = pointer
                    piece = board.state[row-1][col-1]
                    if piece:
                        if piece.color == color:
                            break
                        elif piece.name in [name, QUEEN]:
                            return True
                        else:
                            break
                    pointer = sum_tuple(pointer, direction)

        # Pawn checks
        directions = [(-1,1),(-1,-1)] if color == BLACK else [(1,1),(1,-1)]
        for direction in directions:
            row,col = sum_tuple(king_position, direction)
            if is_valid_position((row,col)):
                piece = board.state[row-1][col-1]
                if piece and piece.name == PAWN and piece.color != color:
                    return True
        
        # King checks?
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                if abs(x) + abs(y) > 0:
                    row,col = sum_tuple(king_position, (x,y))
                    if is_valid_position((row,col)):
                        piece = board.state[row-1][col-1]
                        if piece and piece.name == KING and piece.color != color:
                            return True
        return False

    def get_valid_moves(self, position: tuple, current_board: Board, previous_board: Board) -> list[tuple]:
        """
        Returns all valid moves for the piece in a given position.
        """        
        row,col = position
        piece = current_board.state[row-1][col-1]
        result = []
        if piece:
            for x,y in self.get_available_squares(position, piece):
                if self.validate(Ply().set_piece(piece) \
                                        .set_start(position) \
                                        .set_finish((x,y)),
                                    current_board, previous_board):
                    result.append((x,y))
        return result


    def is_finished(self, current_board: Board, previous_board: Board, color: str) -> bool:
        for position in current_board.active_pieces[color].keys():
            valid_moves = self.get_valid_moves(position, current_board, previous_board)
            if valid_moves:
                return False
        else:
            return True

    def get_available_squares(self, position: tuple, piece: Piece) -> list[tuple]:
        """
        Gets a first approximation for available squares of a given piece in a given
        position. This acts as a filter for the `get_valid_moves` method, so we
        don't have to check all squares for a valid move.
        """
        result = []
        if piece:
            if piece.name == PAWN:
                if piece.color == BLACK:
                    directions = [(-1,0),(-2,0),(-1,1),(-1,-1)]
                else:
                    directions = [(1,0),(2,0),(1,1),(1,-1)]
            elif piece.name == KING:
                directions = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1),(0,2),(0,-2)]
            elif piece.name == KNIGHT:
                directions = KNIGHT_MOVES
            elif piece.name in DIRECTIONS.keys():
                for direction in DIRECTIONS[piece.name]:
                    pointer = sum_tuple(position, direction)
                    while is_valid_position(pointer):
                        result.append(pointer)
                        pointer = sum_tuple(pointer, direction)

        if not result and directions:
            return [square for square in map(sum_tuple, directions, [position]*len(directions)) if is_valid_position(square)]
        else:
            return result
            
