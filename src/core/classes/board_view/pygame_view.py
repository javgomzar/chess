import pygame
from .board_view import BoardView
from ..game_modes import GameMode
from ..pieces import *
from ..color import *
from ..board import Board
from ..check import Check


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

class PygameView(BoardView):
    """
    View for a chess board using pygame.
    """
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

    def __init__(self, game_mode: GameMode, wait_ms: int = 0) -> None:
        pygame.init()
        pygame.display.set_icon(pygame.image.load(self.pieces_paths[White()][Knight]))
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.bg = pygame.image.load(self.background_path)
        self.screen.blit(self.bg, (0,0))
        self.rects = {Position(x,y): pygame.rect.Rect(*self.to_coordinates(Position(x,y)),50,50) for x in range(0,8) for y in range(0,8)}
        self.wait_ms = wait_ms
    
    def get_image(self, piece: Piece) -> pygame.Surface:
        path = self.pieces_paths[piece.color][piece.__class__]
        return pygame.image.load(path)

    def blit_piece(self, piece: Piece, position: Position) -> None:
        self.screen.blit(self.get_image(piece), self.to_coordinates(position))

    def blit_active_pieces(self, board: Board) -> None:
        for piece,position in [(piece,board.get_position(piece)) for piece in board.get_pieces(is_active=True)]:
            self.blit_piece(piece, position)

    def blit_inactive_pieces(self, board: Board) -> None:
        for x,y,color in [(400,0,White()),(400,120,Black())]:
            inactive_pieces = sorted(board.get_pieces(color=color,is_active=False), key=int)
            for piece in inactive_pieces:
                self.screen.blit(self.get_image(piece), (x,y))
                if x == 560:
                    x = 400
                    y += 40
                else:
                    x += 40

    def alert_check(self) -> None:
        print("Check")

    def alert_invalid_move(self) -> None:
        print("Invalid move")

    def show_board(self, board: Board) -> None:
        # Blit background
        self.screen.blit(self.bg, (0,0))

        # Blit red square if the king is under check
        for color in [White(), Black()]:
            king_position = self.to_coordinates(board.get_king_position(color))
            if Check.is_check(color, board):
                pygame.draw.rect(self.screen, red, (*king_position, 50, 50))

        self.blit_active_pieces(board)

        # Draw inactive pieces background 
        pygame.draw.rect(self.screen, black, (400,0,200,400))
        
        self.blit_inactive_pieces(board)
        
        # Update display and wait
        pygame.display.flip()
        pygame.time.wait(self.wait_ms)

    def to_coordinates(self, position: Position) -> tuple:
        return (50*position.col, 350 - 50*position.row)

    def win(self, color: Color) -> None:
        print(f"{color} wins")

    def lose(self, color: Color) -> None:
        print(f"{color} loses")
    
    def draw(self) -> None:
        print(f"It's a draw")
