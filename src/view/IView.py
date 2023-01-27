import abc

from util import IdentifiedObject
from util.publisher_subscriber import Publisher
from controller.IControllerForView import IControllerForView


class IView(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, view_listener: IControllerForView):
        """Set the __controller"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_controller(self) -> IControllerForView:
        """Get the __controller"""
        raise NotImplementedError

    @abc.abstractmethod
    def set_publisher(self, publisher: Publisher):
        """Set the publisher"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher(self) -> Publisher:
        """Get the publisher"""
        raise NotImplementedError

    @abc.abstractmethod
    def detect(self, identified_objects: list):
        """Pass a detected object to the view."""
        raise NotImplementedError
