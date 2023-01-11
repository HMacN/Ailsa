from src.controller.IController import IController
from src.view.IView import IView


class MockController(IController):
    def set_view(self, view: IView):
        pass

    def get_view(self) -> IView:
        pass
