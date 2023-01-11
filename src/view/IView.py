import abc

from controller import Publisher
from controller.IControllerForView import IControllerForView


class IView(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_controller(self, view_listener: IControllerForView):
        """Set the controller"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_controller(self) -> IControllerForView:
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
