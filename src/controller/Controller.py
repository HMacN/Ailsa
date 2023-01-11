from controller.IControllerForView import IControllerForView
from src.controller.IController import IController


class Controller(IController, IControllerForView):
    view = None

    def __init__(self):
        print("Controller Initialised.")

    def set_view(self, given_view):
        self.view = given_view

    def get_view(self):
        return self.view
