from src.view.IView import IView


class View(IView):
    listener = None

    def __init__(self):
        print("View Initialised.")

    def set_listener(self, view_listener):
        self.listener = view_listener

    def get_listener(self):
        return self.listener
