from abc import ABC, abstractmethod

class ActuatorInterface(ABC):

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def toggle(self):
        pass
