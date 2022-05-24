from src.core.classes.color import Black, White
from src.core.classes.players import PygamePlayer
from src.core.classes.game_modes.standard import Standard
from src.core.classes.game import Game
from src.core.classes.board_view import PygameView
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    view = PygameView()
    game = Game(Standard(), view, PygamePlayer(White(), view), PygamePlayer(Black(), view))
    game.main_loop()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        raise err
