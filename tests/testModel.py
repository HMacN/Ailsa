import unittest

from mocks.MockControllerForModel import MockControllerForModel
from model.Model import Model


class ModelTests(unittest.TestCase):

    def test_get_set_controller(self):
        controller = MockControllerForModel()
        model = Model(controller)

        self.assertEqual(controller, model.get_controller())





