import unittest

from controller.Controller import Controller
from mocks.MockController import MockController
from util.IdentifiedObject import IdentifiedObject
from util.publisher_subscriber.Publisher import Publisher
from src.view.View import View


class ViewTests(unittest.TestCase):

    def test_initialises_empty(self):
        controller = MockController()
        view = View(controller)

        self.assertEqual(view.get_publisher(), None)
        self.assertEqual(view.get_controller(), controller)

    def test_get_set_controller(self):
        given_controller = MockController()
        view = View(given_controller)

        registered_controller = view.get_controller()

        self.assertEqual(given_controller, registered_controller)

    def test_get_set_publisher(self):
        view = View(MockController())
        pub = Publisher()

        view.set_publisher(pub)

        self.assertEqual(pub, view.get_publisher())

    def test_identified_objects_are_passed_to_the_controller(self):
        controller = MockController()
        view = View(controller)

        item_1 = IdentifiedObject(1, 1, 2, 2, "test")
        item_2 = IdentifiedObject(5, 5, 2, 2, "test")
        item_3 = IdentifiedObject(9, 9, 2, 2, "test")
        items = [item_1, item_2, item_3]

        view.detect(items)
        returned_items = view.get_detected_items()
        self.assertEqual(items, returned_items)
