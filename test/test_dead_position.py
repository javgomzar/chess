import sys
import unittest as ut

sys.path.append(sys.path[0] + '\\..')

from src.core.classes.finish_conditions import Draw, LockedKings, EnoughPieces
from src.core.classes.position import *
from src.core.classes.color import *
from src.core.classes.board import Board
from src.core.classes.pieces import Pawn, King

class TestDeadPosition(ut.TestCase):
    def test_locked_kings(self):
        board = Board([
            (Pawn(Black(), True), Position.from_notation('a5')),
            (Pawn(Black(), True), Position.from_notation('b4')),
            (Pawn(Black(), True), Position.from_notation('c5')),
            (Pawn(Black(), True), Position.from_notation('e4')),
            (Pawn(Black(), True), Position.from_notation('g5')),
            (Pawn(White(), True), Position.from_notation('a4')),
            (Pawn(White(), True), Position.from_notation('b3')),
            (Pawn(White(), True), Position.from_notation('c4')),
            (Pawn(White(), True), Position.from_notation('e3')),
            (Pawn(White(), True), Position.from_notation('g4')),
            (King(Black(), True), Position.from_notation('e6')),
            (King(White(), True), Position.from_notation('c2'))
        ])

        print(board)


        lk = LockedKings()
        self.assertEqual(lk.handle(None, board), Draw())


    def test_enough_pieces(self):
        board = Board([
            (King(Black(), True), Position.from_notation('e6')),
            (King(White(), True), Position.from_notation('c2')),
            (Pawn(White(), False), None)
        ])

        lk = EnoughPieces()
        self.assertEqual(lk.handle(None, board), Draw())


if __name__ == '__main__':
    ut.main()