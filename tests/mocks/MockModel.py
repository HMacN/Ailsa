from controller.IControllerForModel import IControllerForModel
from model.IModel import IModel


class MockModel(IModel):
    def __init__(self, controller: IControllerForModel):
        pass

    def get_controller(self):
        pass
