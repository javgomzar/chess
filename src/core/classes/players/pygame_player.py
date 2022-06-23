import pygame

from ..board_view import PygameView
from ..board import Board
from ..ply import Ply
from ..color import Color
from ..pieces import Queen

from .player import Player

blue = (0,0,255)

class PygamePlayer(Player):
    def __init__(self, color: Color, pygame_view: PygameView) -> None:
        self.color = color
        self.view = pygame_view
        self.drag = {}

    def input_ply(self, board: Board) -> Ply:
        # if not self.drag:
        #     for piece in board.get_pieces(color=self.color):
        #         self.drag[piece] = False
        from_position = None
        while not from_position:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for position,rect in self.view.rects.items():
                            moving_piece = board.get_piece(position)
                            if rect.collidepoint(event.pos) and moving_piece and moving_piece.color==self.color:
                                from_position = position
                                self.view.blit_square(position, blue, board)
                                valid_moves = self.view.game_mode.get_valid_moves(moving_piece, board)
                                for position in valid_moves:
                                    self.view.blit_square(position, blue, board)
                                pygame.display.flip()
        to_position = None
        while not to_position:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for position,rect in self.view.rects.items():
                            if rect.collidepoint(event.pos):
                                to_position = position
                                self.view.restore_square(from_position, board)
                                for position in valid_moves:
                                    self.view.restore_square(position, board)
                                pygame.display.flip()
        return Ply(self.color, from_position, to_position) 

    def input_promotion(self, board: Board) -> type:
        return Queen