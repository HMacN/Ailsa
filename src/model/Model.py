from controller.IControllerForModel import IControllerForModel
from model.IModel import IModel


class Model(IModel):
    controller: IControllerForModel = None

    def __init__(self, controller: IControllerForModel):
        self.controller = controller

    def get_controller(self):
        return self.controller
