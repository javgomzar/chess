from dataclasses import dataclass
from ..pieces import PieceManager
from .action import Action


@dataclass
class Batch:
    commands : list[Action]

    # def __len__(self):
    #     return len(self.commands)

    def __iter__(self):
        return iter(self.commands)

    def execute(self, piece_manager : PieceManager):
        completed_commands = []
        try:
            for action in self.commands:
                action.execute(piece_manager)
                completed_commands.append(action)
        except Exception as err:
            for action in reversed(completed_commands):
                action.undo(piece_manager)
            raise err

    def undo(self, piece_manager : PieceManager) -> None:
        for action in self.commands:
            action.undo(piece_manager)

    def redo(self, piece_manager : PieceManager) -> None:
        for action in self.commands:
            action.redo(piece_manager)
