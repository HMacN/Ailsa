import abc


class IObjectRecognition(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def go(self, module_handle: str, image_path: str):
        """Handle function for testing"""
        ...
