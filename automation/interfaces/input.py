from abc import ABC, abstractmethod

class InputInterface(ABC):
    @abstractmethod
    def worker():
        pass

    @abstractmethod
    def run():
        pass


