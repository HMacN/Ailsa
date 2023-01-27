import unittest

from controller.IControllerForModel import IControllerForModel
from mocks.MockController import MockController
from mocks.MockModel import MockModel
from model.Model import Model
from src.controller.Controller import Controller
from tests.mocks.MockView import MockView
from util.IdentifiedObject import IdentifiedObject


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

    def test_detect_and_retrieve_objects(self):
        controller = Controller()
        model_controller: IControllerForModel = controller
        model = Model(model_controller)
        controller.set_model(model)

        item_1 = IdentifiedObject(1, 1, 2, 2, "test")
        item_2 = IdentifiedObject(5, 5, 2, 2, "test")
        item_3 = IdentifiedObject(9, 9, 2, 2, "test")
        items = [item_1, item_2, item_3]

        controller.detect(items)
        returned_items = controller.get_detected_items()

        self.assertEqual(items, returned_items)



