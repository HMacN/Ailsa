import unittest

from mocks.MockController import MockController
from model.Model import Model
from util.IdentifiedObject import IdentifiedObject


class ModelTests(unittest.TestCase):

    def test_get_set_controller(self):
        controller = MockController()
        model = Model(controller)

        self.assertEqual(controller, model.get_controller())

    def test_register_new_detected_object(self):
        controller = MockController()
        model = Model(controller)
        item = IdentifiedObject(1, 1, 1, 1, "test")

        model.detect(item)

        # TODO pass in a list of detected objects and then check that the new item is added to the list.
