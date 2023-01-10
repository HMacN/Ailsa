import abc

from src.controller.IController import IController


class IModel(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_listener(self, controller: IController):
        """Set the controller"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_listener(self) -> IController:
        """Get the controller"""
        raise NotImplementedError
