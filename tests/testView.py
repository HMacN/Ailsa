import unittest

from controller.Publisher import Publisher
from tests.Mocks.MockControllerForView import MockControllerForView
from src.view.View import View


class ViewTests(unittest.TestCase):

    def test_initialises_empty(self):
        view = View()

        self.assertEqual(view.get_publisher(), None)
        self.assertEqual(view.get_controller(), None)

    def test_get_set_controller(self):
        given_controller = MockControllerForView()
        view = View()

        view.set_controller(given_controller)

        registered_controller = view.get_controller()

        self.assertEqual(given_controller, registered_controller)

    def test_get_set_publisher(self):
        view = View()
        pub = Publisher()

        view.set_publisher(pub)

        self.assertEqual(pub, view.get_publisher())
