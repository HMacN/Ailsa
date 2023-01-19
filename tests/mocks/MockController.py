from controller.IControllerForView import IControllerForView
from model.IModel import IModel
from src.controller.IController import IController
from src.view.IView import IView
from util.IdentifiedObject import IdentifiedObject
from controller.IControllerForModel import IControllerForModel


class MockController(IController, IControllerForView, IControllerForModel):
    def __init__(self):
        self.detected_object = None

    def get_given_identified_object(self) -> IdentifiedObject:
        return self.detected_object

    def new_detected_object(self, detected_object):
        self.detected_object = detected_object

    def set_model(self, model: IModel):
        pass

    def get_model(self) -> IView:
        pass

    def set_view(self, view: IView):
        pass

    def get_view(self) -> IView:
        pass
