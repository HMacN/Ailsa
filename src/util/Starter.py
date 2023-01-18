from controller.Controller import Controller
from controller.IController import IController
from controller.IControllerForView import IControllerForView
from view.IView import IView
from view.View import View


class Starter:
    controller: IController = None
    view_controller: IControllerForView = None
    view: IView = None

    def __int__(self):
        self.controller = Controller()

        print("Controller: " + str(self.controller))  # todo remove

        self.view_controller = self.controller

        print("View Controller: " + str(self.view_controller))  # todo remove

        self.view = View(self.view_controller)

        print("View: " + str(self.view))  # todo remove

    def get_controller(self) -> IController:
        return self.controller

    def get_view(self) -> IView:
        return self.view
