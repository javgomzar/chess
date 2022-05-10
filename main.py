from src.core.classes.color import Black, White
from src.core.classes.players.terminal_player import TerminalPlayer
from src.core.classes.game_modes.standard import Standard
from src.core.classes.game import Game
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    game = Game(Standard(), TerminalPlayer(White()), TerminalPlayer(Black()))
    game.main_loop()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        raise err
