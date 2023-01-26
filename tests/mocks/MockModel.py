from controller.IControllerForModel import IControllerForModel
from model.IModel import IModel
from util.IdentifiedObject import IdentifiedObject


class MockModel(IModel):

    def __init__(self, controller: IControllerForModel):
        pass

    def get_controller(self):
        pass

    def detect(self, item: IdentifiedObject):
        pass
