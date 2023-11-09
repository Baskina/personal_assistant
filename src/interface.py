from abc import abstractmethod, ABC


class UserInterface(ABC):
    def __init__(self):
        self.data = None

    @abstractmethod
    def show_result(self, data):
        pass

    @abstractmethod
    def info(self):
        pass


class Terminal(UserInterface):
    def __init__(self):
        self.data = None

    def show_result(self, result):
        print(result)

    def info(self):
        print("I am a terminal interface")
