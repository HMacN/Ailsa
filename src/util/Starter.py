from controller.Controller import Controller
from controller.IController import IController
from controller.IControllerForView import IControllerForView
from view.IView import IView
from view.View import View


class Starter:

    def __init__(self):
        self.controller = Controller()
        self.view = View(self.controller)

    def get_controller(self) -> IController:
        return self.controller

    def get_view(self) -> IView:
        return self.view
