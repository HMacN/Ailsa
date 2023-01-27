import abc

from controller.IControllerForModel import IControllerForModel
from model.DetectedObjectRegister import DetectedObjectRegister
from util.IdentifiedObject import IdentifiedObject


class IModel(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, controller: IControllerForModel):
        """Constructor that requires a Controller to be passed in."""
        ...

    @abc.abstractmethod
    def get_controller(self):
        """Getter for the Controller."""
        ...

    @abc.abstractmethod
    def detect(self, items: list):
        """Pass detected objects into the model."""
        ...

    @abc.abstractmethod
    def get_detected_items(self) -> list:
        """Get all items recorded by the model"""
        ...
