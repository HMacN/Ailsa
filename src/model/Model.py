from controller.IControllerForModel import IControllerForModel
from model.DetectedObjectRegister import DetectedObjectRegister
from model.IModel import IModel


class Model(IModel):

    def __init__(self, controller: IControllerForModel):
        self.__register: DetectedObjectRegister = DetectedObjectRegister()
        self.__controller: IControllerForModel = controller

    def get_controller(self):
        return self.__controller

    def detect(self, items: list):
        for i in items:
            self.__register.add(i)

    def get_detected_items(self):
        return self.__register.get_all()
