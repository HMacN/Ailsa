import abc


class IControllerForView(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def detect(self, detected_objects: list):
        """Add a newly detected objects to the __controller"""
        ...

    @abc.abstractmethod
    def get_detected_items(self):
        """Returns all unique detected items"""
        ...
