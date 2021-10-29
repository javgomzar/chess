from src.config.constants import BLACK, CASTLE, EN_PASSANT, INVALID_ACTION, MOVE, PROMOTE, WHITE, LEFT, RIGHT, TOWER, EMPTY_BOARD_STRING, EMPTY_SQ_MSG, INIT_BOARD, KING
from src.core.classes.Piece import Piece
from src.core.classes.Ply import Ply

class Board():
    """
    Class for a chess board. Initializes as an empty board. To set it to the
    standard chess configuration use the method `init_std_board`.
    """
    def __init__(self) -> None:
        self.state = [[None for col in range(0,8)] for row in range(0,8)]
        self.removed_pieces = []
        self.active_pieces = {
            BLACK: {},
            WHITE: {}
        }
        self.king_position = {
            BLACK: None,
            WHITE: None
        }
        self.king_moved = {
            BLACK: False,
            WHITE: False
        }
        self.tower_moved = {
            BLACK:{
                LEFT: False,
                RIGHT: False
            },
            WHITE: {
                LEFT: False,
                RIGHT: False
            }
        }


    def __str__(self) -> str:
        result = EMPTY_BOARD_STRING
        for row in range(0,8):
            for col in range(0,8):
                piece = self.state[row][col]
                if piece:
                    symbol = str(piece)
                else:
                    symbol = "  "
                result = result.replace(str(row+1) + str(col+1), symbol)
        return result


    def __repr__(self) -> str:
        return "\n".join(map(str, self.state))


    def add_piece(self, piece: Piece, position: tuple):
        """
        Adds a piece to the board and returns `self`.
        """
        row,col = position
        self.state[row-1][col-1] = piece
        self.active_pieces[piece.color][position] = piece
        return self


    def remove_piece(self, position: tuple):
        """
        Removes a piece from the board and returns `self`.
        """
        row,col = position
        piece = self.state[row-1][col-1]
        if piece:
            self.active_pieces[piece.color].pop(position)
            self.removed_pieces.append(piece)
            self.state[row-1][col-1] = None
        else:
            return self


    def move_piece(self, start: tuple, finish: tuple):
        """
        Moves a piece in the board and returns `self`.
        """
        start_row, start_col = start
        finish_row, finish_col = finish
        piece = self.state[start_row-1][start_col-1]

        # If there is a piece in the destination, we remove it
        if not piece:
            raise Exception(EMPTY_SQ_MSG)
        elif self.state[finish_row-1][finish_col-1]:
            self.remove_piece(finish)

        # Then we move the piece
        self.add_piece(piece, finish)
        self.remove_piece(start)

        # Here we keep track of movements for castling
        if piece.name == KING:
            if not self.king_moved[piece.color]:
                self.king_moved[piece.color] = True
            self.king_position[piece.color] = finish
        elif piece.name == TOWER:
            if start_col in [1,8]:
                side = LEFT if start_col == 1 else RIGHT
                if not self.tower_moved[piece.color][side]:
                    self.tower_moved[piece.color][side] = True

        return self


    def init_std_board(self):
        """
        Initiates the standard chess configuration.
        """
        for position in INIT_BOARD.keys():
            row,col = position
            square = INIT_BOARD[position]
            if square:
                self.add_piece(Piece(square['piece'], square['color']), position)
            else:
                self.state[row-1][col-1] = None
        self.king_position[WHITE] = (1,5)
        self.king_position[BLACK] = (8,5)
        return self


    def promote(self, position: tuple, piece_name: str):
        """
        Promotes the piece in a position to the type given by `piece_name` and returns `self`.
        """
        row,col = position
        piece = self.state[row-1][col-1]
        if piece: 
            piece.name = piece_name


    def execute_action(self, ply: Ply):
        """
        Executes a possible outcome of a chess movement. The action should be in the `action`
        property of the ply argument. There are four possible actions: 
            - `MOVE`: Moves a piece.
            - `PROMOTE`: Promotes a pawn.
            - `EN_PASSANT`: Moves a pawn and then removes the pawn behind it.
            - `CASTLE`: Moves the king and tower acording to the castling rules.
        """
        action = ply.action

        if action == MOVE:
            self.move_piece(ply.start,ply.finish)

        elif action == PROMOTE:
            self.move_piece(ply.start, ply.finish)
            self.promote(ply.finish, ply.promotion)

        elif action == EN_PASSANT:
            self.move_piece(ply.start,ply.finish)
            if ply.color == BLACK:
                self.remove_piece((ply.finish[0]+1, ply.finish[1]))
            else:
                self.remove_piece((ply.finish[0]-1, ply.finish[1]))

        elif action == CASTLE:
            row = 8 if ply.color == BLACK else 1
            Dy = ply.finish[1] - ply.start[1]
            self.move_piece(ply.start, ply.finish)
            if Dy > 0:
                self.move_piece((row,8), (row,6))
            else:
                self.move_piece((row,1), (row,4))

        else:
            raise Exception(INVALID_ACTION)
