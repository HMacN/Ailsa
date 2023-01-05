class AilsaView:
    controller = None

    def __init__(self):
        print("View Initialised.")

    def register_controller(self, controller):
        self.controller = controller

    def get_controller(self):
        return self.controller
