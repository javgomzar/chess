import pygame
from .board_view import BoardView
from ..pieces import *
from ..color import *
from ..board import Board

white = (255,255,255)
black = (0,0,0)

class PygameView(BoardView):
    height: int = 400
    width: int = 600
    background_path: str = "./media/board.png"
    pieces_paths: dict = {
        Black(): {
            Pawn: "./media/black/pawn.png",
            Bishop: "./media/black/bishop.png",
            King: "./media/black/king.png",
            Knight: "./media/black/knight.png",
            Queen: "./media/black/queen.png",
            Rook: "./media/black/rook.png"
        },
        White(): {
            Pawn: "./media/white/pawn.png",
            Bishop: "./media/white/bishop.png",
            King: "./media/white/king.png",
            Knight: "./media/white/knight.png",
            Queen: "./media/white/queen.png",
            Rook: "./media/white/rook.png"
        }
    }

    def __init__(self, wait_miliseconds: int = 0) -> None:
        pygame.init()
        pygame.display.set_icon(pygame.image.load(self.pieces_paths[White()][Knight]))
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.bg = pygame.image.load(self.background_path)
        self.screen.blit(self.bg, (0,0))
        self.rects = {Position(x,y): pygame.rect.Rect(*self.to_coordinates(Position(x,y)),50,50) for x in range(0,8) for y in range(0,8)}
        self.wait_miliseconds = wait_miliseconds
    
    def get_image(self, piece: Piece) -> pygame.Surface:
        path = self.pieces_paths[piece.color][piece.__class__]
        return pygame.image.load(path)

    def show_board(self, board: Board) -> None:
        self.screen.blit(self.bg, (0,0))
        for x in range(0,8):
            for y in range(0,8):
                position = Position(x,y)
                piece = board.get_piece(position)
                if piece:
                    self.screen.blit(self.get_image(piece), self.to_coordinates(position))
        pygame.draw.rect(self.screen, black, (400,0,200,400))
        x,y = 400,0
        white_inactive_pieces = board.get_pieces(color=White(),is_active=False)
        white_inactive_pieces = sorted(white_inactive_pieces, key=lambda x: int(x))
        for piece in white_inactive_pieces:
            self.screen.blit(self.get_image(piece), (x,y))
            if x == 560:
                x = 400
                y += 40
            else:
                x += 40
        x,y = 400,120
        black_inactive_pieces = board.get_pieces(color=Black(),is_active=False)
        black_inactive_pieces = sorted(black_inactive_pieces, key=lambda x: int(x))
        for piece in black_inactive_pieces:
            self.screen.blit(self.get_image(piece), (x,y))
            if x == 560:
                x = 400
                y += 40
            else:
                x += 40
        
        pygame.display.flip()
        pygame.time.wait(self.wait_miliseconds)

    def to_coordinates(self, position: Position) -> tuple:
        return (50*position.col, 350 - 50*position.row)

    def win(self, color: Color) -> None:
        print(f"{color} wins")

    def lose(self, color: Color) -> None:
        print(f"{color} loses")
    
    def draw(self) -> None:
        print(f"It's a draw")
