import queue
import threading

class EventEngine():
    def __init__(self):
        self.__queue = queue.Queue()
        self.subscribers =  {}

    def new_event(self, event):
        self.__queue.put(event)

    def add_subscriber(self, event, callback, *args, **kwargs):
        if event not in self.subscribers:
            self.subscribers[event] = []

        self.subscribers[event].append((callback, args, kwargs))

    def _process_event(self, event):
        if event in self.subscribers:
            for callback in self.subscribers[event]:
                callback[0](*callback[1])

    def worker(self):
        while True:
            while not self.__queue.empty():
                event = self.__queue.get()
                print('got event')
                print(event)
                self._process_event(event)

    def run(self):
        print('Starting event engine')
        thread_event_engine = threading.Thread(target=self.worker, daemon=True).start()
