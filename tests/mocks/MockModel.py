from controller.IControllerForModel import IControllerForModel
from model.DetectedObjectRegister import DetectedObjectRegister
from model.IModel import IModel
from util.IdentifiedObject import IdentifiedObject


class MockModel(IModel):

    def get_detected_items(self) -> list:
        pass

    def set_register(self, register: DetectedObjectRegister):
        pass

    def __init__(self, controller: IControllerForModel):
        pass

    def get_controller(self):
        pass

    def detect(self, item: IdentifiedObject):
        pass
