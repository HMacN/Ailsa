import abc


class IObjectRecognition(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def go(self):
        """Handle function for testing"""
        ...
