from abc import ABC, abstractmethod

from ..finish_conditions import FinalState
from ..pieces import Piece
from ..ply import Ply
from ..board import Board


class GameMode(ABC):
    @abstractmethod
    def init_board(self) -> Board:
        pass

    @abstractmethod
    def validate(self, ply: Ply, board: Board) -> bool:
        pass

    @abstractmethod
    def is_finished(self, ply: Ply, board: Board) -> FinalState:
        pass

    def get_valid_moves(self, piece: Piece, board: Board) -> list[tuple]:
        """
        Returns all valid moves for a piece in a given board.
        """
        result = []
        from_position = board.get_position(piece)
        for possible_move in piece.available_positions(from_position):
            if self.validate(Ply(piece.color, from_position, possible_move), board):
                result.append(possible_move)
        return result
