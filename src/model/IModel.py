import abc

from controller.IControllerForModel import IControllerForModel
from src.controller.IController import IController


class IModel(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, controller: IControllerForModel):
        """Constructor that requires a Controller to be passed in."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_controller(self):
        """Getter for the Controller."""
        raise NotImplementedError
