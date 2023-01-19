from controller.Controller import Controller
from controller.IController import IController
from controller.IControllerForView import IControllerForView
from model.IModel import IModel
from model.Model import Model
from view.IView import IView
from view.View import View


class Starter:

    def __init__(self):
        self.controller: IController = Controller()
        self.view: IView = View(self.controller)
        self.model: IModel = Model(self.controller)
        self.controller.set_view(self.view)
        self.controller.set_model(self.model)

    def get_controller(self) -> IController:
        return self.controller

    def get_view(self) -> IView:
        return self.view

    def get_model(self):
        return self.model
