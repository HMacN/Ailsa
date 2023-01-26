import abc

from controller.IControllerForModel import IControllerForModel
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
    def detect(self, item: IdentifiedObject):
        """Pass a detected object into the model."""
        ...
