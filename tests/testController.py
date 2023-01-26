import unittest

from controller.IControllerForModel import IControllerForModel
from mocks.MockController import MockController
from mocks.MockModel import MockModel
from src.controller.Controller import Controller
from tests.mocks.MockView import MockView


class ControllerTests(unittest.TestCase):

    def test_controller_initialises_empty(self):
        controller = Controller()

        self.assertEqual(None, controller.get_view())
        self.assertEqual(None, controller.get_model())

    def test_get_set_view(self):
        given_view = MockView(MockController())
        controller = Controller()

        controller.set_view(given_view)

        registered_view = controller.get_view()

        self.assertEqual(given_view, registered_view)

    def test_get_set_model(self):
        given_model = MockModel(MockController())
        controller = Controller()

        controller.set_model(given_model)

        registered_model = controller.get_model()

        self.assertEqual(given_model, registered_model)





