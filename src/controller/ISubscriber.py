import abc


class ISubscriber(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def notify(self):
        """Notify the listener about a publication."""
        raise NotImplementedError
