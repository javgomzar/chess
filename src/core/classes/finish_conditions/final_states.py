from src.core.metaclasses.singleton import Singleton

class FinalState(Exception, metaclass=Singleton):
    pass

class Draw(FinalState):
    pass

class Win(FinalState):
    pass
