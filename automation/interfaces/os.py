from abc import ABC, abstractmethod

class OSInterface(ABC):
    @abstractmethod
    def process_exists():
        pass

    @abstractmethod
    def process_launch():
        pass

    @abstractmethod
    def is_locked():
        pass

    @abstractmethod
    def lock():
        pass

    @abstractmethod
    def unlock():
        pass

    @abstractmethod
    def switch_display():
        pass

    @abstractmethod
    def switch_audio():
        pass

    @abstractmethod
    def move_mouse():
        pass
