from ..pieces.piece_manager import PieceManager
from .action import Action


class ActionController(PieceManager):
    """
    Controller for executing actions on a board. This class
    will keep a history of the actions executed on a board, 
    and will be able to undo and redo them.
    """
    undo_stack : list[Action]
    redo_stack : list[Action]

    def __init__(self):
        super().__init__()
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, action : Action) -> None:
        """Executes an action on a board."""
        action.process(self)
        action.execute(self)
        self.clear()
        self.undo_stack.append(action)

    def undo(self) -> None:
        """Undoes the last action."""
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        action.undo(self)
        self.redo_stack.append(action)

    def redo(self) -> None:
        """Redoes the last undone action."""
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        action.redo(self)
        self.undo_stack.append(action)

    def undo_all(self) -> None:
        """Undoes all actions."""
        for n in range(0,len(self.undo_stack)):
            self.undo()

    def redo_all(self) -> None:
        """Redoes all undone actions."""
        for n in range(0,len(self.redo_stack)):
            self.redo()

    def clear(self) -> None:
        """Clears redo stack."""
        self.redo_stack.clear()

    def roll_back(self) -> None:
        """Undoes and forgets the last action."""
        self.undo()
        self.clear()

    def try_action(self, action: Action):
        """
        Executes an action on a board but instead of changing it, it
        returns a copy of the board with the action executed on it.
        """
        self.execute(action)
        result = self.copy()
        self.roll_back()
        return result

    def get_previous_board(self):
        """
        Returns a copy of the board in its previous state.
        """
        self.undo()
        board = self.copy()
        self.redo()
        return board

    def last_action(self):
        """
        Returns the last action executed on the board.
        """
        return self.undo_stack[-1]
