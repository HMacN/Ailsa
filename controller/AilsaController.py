class AilsaController:
    view = None

    def __init__(self):
        print("Controller Initialised.")

    def register_view(self, given_view):
        self.view = given_view

    def get_view(self):
        return self.view
