import re

from src.utils import remove_empty
from .batch_player import BatchPlayer
from ..color import Color, White
from ..ply import Ply, ply_from_notation
from ..board import Board


class PGNPlayer(BatchPlayer):
    def __init__(self, color: Color, path: str):
        file = open(path, 'r')
        raw_text = file.read()
        clean_text = re.sub(r"\[.*\]\n*", "", raw_text).replace("\n", " ")
        print(clean_text)
        clean_text = remove_empty(re.sub(r"\d*\.", ";", clean_text).split(";"))
        notation_list = list(map(lambda x: x.split(' ')[0 if color == White() else 1], clean_text))

        if re.match(r"\d+\-\d+", notation_list[-1]):
            notation_list.pop()

        print(notation_list)

        file.close()
        super().__init__(color, notation_list)

    def input_ply(self, board: Board) -> Ply:
        return ply_from_notation(self.color, super().input_ply(board), board)