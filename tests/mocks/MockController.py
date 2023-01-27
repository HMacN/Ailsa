from controller.IControllerForView import IControllerForView
from model.IModel import IModel
from src.controller.IController import IController
from src.view.IView import IView
from util.IdentifiedObject import IdentifiedObject
from controller.IControllerForModel import IControllerForModel


class MockController(IController, IControllerForView, IControllerForModel):
    def get_detected_items(self):
        return self.detected_objects

    def __init__(self):
        self.detected_objects = None

    def get_given_identified_object(self) -> IdentifiedObject:
        return self.detected_objects

    def detect(self, detected_objects):
        self.detected_objects = detected_objects

    def set_model(self, model: IModel):
        pass

    def get_model(self) -> IView:
        pass

    def set_view(self, view: IView):
        pass

    def get_view(self) -> IView:
        pass
