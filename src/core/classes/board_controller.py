from dataclasses import dataclass, field
from src.core.classes.board import Board
from src.core.classes.action import Action

@dataclass
class BoardController():
    board : Board = field(default_factory=Board)
    undo_stack : list[Action] = field(default_factory=list)
    redo_stack : list[Action] = field(default_factory=list)

    def execute(self, action : Action) -> None:
        action.execute(self.board)
        self.redo_stack.clear()
        self.undo_stack.append(action)

    def undo(self) -> None:
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        action.undo(self.board)
        self.redo_stack.append(action)

    def redo(self) -> None:
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        action.redo(self.board)
        self.undo_stack.append(action)

    def undo_all(self) -> None:
        for n in range(0,len(self.undo_stack)):
            self.undo()

    def redo_all(self) -> None:
        for n in range(0,len(self.redo_stack)):
            self.redo()

    def clear(self) -> None:
        self.redo_stack = []

    def roll_back(self) -> None:
        self.undo()
        self.clear()

    def get_previous_board(self) -> Board:
        self.undo()
        board = self.board.copy()
        self.redo()
        return board
