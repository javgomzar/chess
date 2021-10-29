from src.core.classes.Game import Game


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        raise err
