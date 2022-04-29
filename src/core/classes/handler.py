from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self) -> None:
        self._next = None

    def set_next(self, rule) -> None:
        self._next = rule

    @abstractmethod
    def handle(self, *args) -> None:
        pass
