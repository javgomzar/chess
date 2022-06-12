from .finish_condition import FinishCondition
from .final_states import Draw, FinalState
from ..ply import Ply
from ..board import Board
from ..pieces import Pawn, King
from ..color import *
from ..error_classes import PositionError



class LockedKings(FinishCondition):
    def process(self, ply: Ply, board: Board) -> None:
        self.pawns = board.get_pieces(is_active=True,piece_type=Pawn)

        unavailable_positions = {color: [] for color in [Black(), White()]}
        for pawn in self.pawns:
            pawn_position = board.get_position(pawn)
            unavailable_positions[pawn.color].append(pawn_position)
            for position in pawn.available_captures(pawn_position):
                unavailable_positions[pawn.color.opposite_color()].append(position)

        self.unavailable_positions = {color: unavailable_positions[color] for color in [Black(), White()]}
        self.seeds = {color: [position for position in self.unavailable_positions[color] if position.col == 0 or position.col == 7] for color in [Black(),White()]}

        print(self.unavailable_positions)
        print(self.seeds)

    def condition(self, ply: Ply, board: Board) -> bool:
        # Only pawns left
        if len(self.pawns) != len(board.get_pieces(is_active=True, exclude_type=King)):
            return False

        # All pawns locked
        for pawn in self.pawns:
            position = board.get_position(pawn)
            # A pawn is not locked if it doesn't have another piece in front of it or it can capture other pieces
            front = board.get_piece(position + pawn.color.pawn_direction)
            captures = [piece for piece in self.pawns if board.get_position(piece) in pawn.available_captures(position) and piece.color != pawn.color]
            if not front or captures:
                return False

        paths = 0
        for color in [Black(), White()]:
            print(f"Color: {color}")
            for seed in self.seeds[color]:
                print(f"Seed: {seed}")
                self.seeds[color].remove(seed)
                if self.path_established(seed, color):
                    paths += 1
                    break

        if paths == 2:
            return True
                    

    def get_final_state(self, ply: Ply, board: Board) -> FinalState:
        return Draw()

    def next_positions(self, from_position: Position, color: Color) -> list[Position]:
        result = []
        for vector in [Vector(0,1), Vector(1,0), Vector(0,-1), Vector(-1,0)]:
            try:
                position = from_position + vector
            except PositionError:
                pass
            else:
                if position in self.unavailable_positions[color]:
                    result.append(position)
        return result

    def exists_far_enough(self, seed: Position, passed_nodes: list[Position]) -> bool:
        for node in passed_nodes:
            if (node - seed).col > 1:
                return True
        return False

    def path_established(self, seed: Position, color: Color) -> bool:
        available_nodes = [seed]
        passed_nodes = []
        destinations = self.seeds[color]
        far_enough = False

        while True:
            node = available_nodes.pop()
            if not far_enough:
                far_enough = self.exists_far_enough(seed, passed_nodes)
            if node in destinations and far_enough:
                passed_nodes.append(node)
                return True
            new_nodes = list(filter(lambda x: x not in passed_nodes and x not in available_nodes, self.next_positions(node, color)))
            available_nodes += new_nodes
            passed_nodes.append(node)
            if not available_nodes:
                return False
