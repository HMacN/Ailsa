from controller import Publisher
from src.view import IViewListener
from src.view.IView import IView


class MockView(IView):
    def set_publisher(self, publisher: Publisher):
        pass

    def get_publisher(self) -> Publisher:
        pass

    def get_listener(self) -> IViewListener:
        pass

    def set_listener(self, view_listener: IViewListener):
        pass
