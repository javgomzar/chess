
class Board():

    state : list

    def __init__(self) -> None:
        self.state = [[None for col in range(1,9)] for row in range(1,9)]

    def __str__(self) -> str:
        pass
        
    def __repr__(self) -> str:
        pass
