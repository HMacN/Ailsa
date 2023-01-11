from controller import Publisher, IControllerForView
from src.view.IView import IView


class MockView(IView):
    def set_publisher(self, publisher: Publisher):
        pass

    def get_publisher(self) -> Publisher:
        pass

    def get_controller(self) -> IControllerForView:
        pass

    def set_controller(self, view_listener: IControllerForView):
        pass
