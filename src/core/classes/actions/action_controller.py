from ..pieces.piece_manager import PieceManager
from .action import Action

class ActionController(PieceManager):
    undo_stack : list[Action]
    redo_stack : list[Action]

    def __init__(self):
        super().__init__()
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, action : Action) -> None:
        action.execute(self)
        self.clear()
        self.undo_stack.append(action)

    def undo(self) -> None:
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        action.undo(self)
        self.redo_stack.append(action)

    def redo(self) -> None:
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        action.redo(self)
        self.undo_stack.append(action)

    def undo_all(self) -> None:
        for n in range(0,len(self.undo_stack)):
            self.undo()

    def redo_all(self) -> None:
        for n in range(0,len(self.redo_stack)):
            self.redo()

    def clear(self) -> None:
        self.redo_stack.clear()

    def roll_back(self) -> None:
        self.undo()
        self.clear()

    def try_action(self, action: Action):
        self.execute(action)
        result = self.copy()
        self.roll_back()
        return result

    def get_previous_board(self):
        self.undo()
        board = self.copy()
        self.redo()
        return board

    def last_action(self):
        return self.undo_stack[-1]
