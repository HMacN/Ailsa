from controller.IControllerForModel import IControllerForModel
from model.IModel import IModel
from util.IdentifiedObject import IdentifiedObject


class Model(IModel):

    def __init__(self, controller: IControllerForModel):
        self.controller: IControllerForModel = controller

    def get_controller(self):
        return self.controller

    def detect(self, item: IdentifiedObject):
        pass
