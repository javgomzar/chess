from typing import Protocol


class State(Protocol):
    def handle(self):
        pass
