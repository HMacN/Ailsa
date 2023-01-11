import unittest

from controller.Publisher import Publisher
from tests.Mocks.MockViewListener import MockViewListener
from src.view.View import View


class ViewTests(unittest.TestCase):

    def test_initialises_empty(self):
        view = View()

        self.assertEqual(view.get_publisher(), None)
        self.assertEqual(view.get_listener(), None)

    def test_get_set_listener(self):
        given_listener = MockViewListener()
        view = View()

        view.set_listener(given_listener)

        registered_listener = view.get_listener()

        self.assertEqual(given_listener, registered_listener)

    def test_get_set_publisher(self):
        view = View()
        pub = Publisher()

        view.set_publisher(pub)

        self.assertEqual(pub, view.get_publisher())
