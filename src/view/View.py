from controller import Publisher
from src.view.IView import IView


class View(IView):
    listener = None
    publisher: Publisher = None

    def __init__(self):
        print("View Initialised.")
        self.listener = None

    def set_listener(self, view_listener):
        self.listener = view_listener

    def get_listener(self):
        return self.listener

    def set_publisher(self, publisher: Publisher):
        self.publisher = publisher

    def get_publisher(self) -> Publisher:
        return self.publisher
