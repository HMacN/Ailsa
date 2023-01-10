from src.view import IViewListener
from src.view.IView import IView


class MockView(IView):
    def get_listener(self) -> IViewListener:
        pass

    def set_listener(self, view_listener: IViewListener):
        pass
