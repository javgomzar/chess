from dataclasses import dataclass
from src.core.classes.board import Board
from src.core.classes.actions.action import Action


@dataclass
class Batch:
    commands : list[Action]

    def __len__(self):
        return len(self.commands)

    def __iter__(self):
        return iter(self.commands)

    def execute(self, board : Board):
        completed_commands = []
        try:
            for action in self.commands:
                action.execute(board)
                completed_commands.append(action)
        except Exception as err:
            for action in reversed(completed_commands):
                action.undo(board)
            raise err

    def undo(self, board : Board) -> None:
        for action in self.commands:
            action.undo(board)

    def redo(self, board : Board) -> None:
        for action in self.commands:
            action.redo(board)
