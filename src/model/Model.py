from controller.IController import IController
from model.IModel import IModel


class Model(IModel):
    def set_listener(self, controller: IController):
        pass

    def get_listener(self) -> IController:
        pass
