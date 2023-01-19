import abc


class IControllerForView(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def new_detected_object(self, detected_object):
        """Add a newly detected object to the controller"""
        ...
