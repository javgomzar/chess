from src.config.constants import BLACK_NAMES, WHITE_NAMES
from src.core.classes.color import Black, Color, White

class Input:
    @classmethod
    def color(self, text: str) -> Color:
        if text.upper() in BLACK_NAMES:
            return Black()
        elif text.upper() in WHITE_NAMES:
            return White()
        raise ValueError()
