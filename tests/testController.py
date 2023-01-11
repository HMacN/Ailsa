import unittest

from tests.mocks.MockControllerForView import MockControllerForView
from src.controller.Controller import Controller
from tests.mocks.MockView import MockView


class ControllerTests(unittest.TestCase):
    def test_get_set_view(self):
        given_view = MockView(MockControllerForView())
        controller = Controller()

        controller.set_view(given_view)

        registered_view = controller.get_view()

        self.assertEqual(registered_view, given_view)


