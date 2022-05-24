import pygame

from ..board_view import PygameView
from .player import Player
from ..board import Board
from ..ply import Ply
from ..color import Color
from ..pieces import Queen


class PygamePlayer(Player):
    def __init__(self, color: Color, pygame_view: PygameView) -> None:
        self.color = color
        self.view = pygame_view
        self.drag = {}

    def input_ply(self, board: Board) -> Ply:
        if not self.drag:
            for piece in board.get_pieces(color=self.color):
                self.drag[piece] = False
        from_position = None
        while not from_position:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for position,rect in self.view.rects.items():
                            if rect.collidepoint(event.pos):
                                from_position = position
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
        return Ply(self.color, from_position, to_position)

    def input_promotion(self, board: Board) -> type:
        return Queen