from controller import IdentifiedObject
from controller.IControllerForView import IControllerForView


class MockControllerForView(IControllerForView):

    detected_object = None

    def __init__(self):
        self.detected_object = None

    def get_given_identified_object(self) -> IdentifiedObject:
        return self.detected_object

    def new_detected_object(self, detected_object):
        self.detected_object = detected_object
