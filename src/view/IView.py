import abc

from controller import Publisher
from src.view.IViewListener import IViewListener


class IView(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_listener(self, view_listener: IViewListener):
        """Set the controller"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_listener(self) -> IViewListener:
        """Get the controller"""
        raise NotImplementedError

    @abc.abstractmethod
    def set_publisher(self, publisher: Publisher):
        """Set the publisher"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher(self) -> Publisher:
        """Get the publisher"""
        raise NotImplementedError
