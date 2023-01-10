import unittest

from tests.Mocks.MockViewListener import MockViewListener
from src.view.View import View


class ViewTests(unittest.TestCase):

    def test_get_set_listener(self):
        given_listener = MockViewListener()
        view = View()

        view.set_listener(given_listener)

        registered_listener = view.get_listener()

        self.assertEqual(given_listener, registered_listener)

