from controller import Publisher
from controller.IControllerForView import IControllerForView
from src.view.IView import IView


class View(IView):
    listener = None
    publisher: Publisher = None

    def __init__(self):
        print("View Initialised.")
        self.listener = None

    def set_controller(self, view_listener: IControllerForView):
        self.listener = view_listener

    def get_controller(self) -> IControllerForView:
        return self.listener

    def set_publisher(self, publisher: Publisher):
        self.publisher = publisher

    def get_publisher(self) -> Publisher:
        return self.publisher
