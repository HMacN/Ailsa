from controller.IControllerForModel import IControllerForModel
from model.IModel import IModel


class Model(IModel):

    def __init__(self, controller: IControllerForModel):
        self.controller: IControllerForModel = controller

    def get_controller(self):
        return self.controller
