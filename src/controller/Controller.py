from controller.IControllerForView import IControllerForView
from model.IModel import IModel
from src.controller.IController import IController
from util.IdentifiedObject import IdentifiedObject
from view.IView import IView


class Controller(IController, IControllerForView):

    def __init__(self):
        self.view: IView = None
        self.model: IModel = None

    def set_view(self, given_view: IView):
        self.view = given_view

    def get_view(self) -> IView:
        return self.view

    def new_detected_object(self, detected_object: IdentifiedObject):
        pass

    def set_model(self, given_model: IModel):
        self.model = given_model

    def get_model(self) -> IModel:
        return self.model
