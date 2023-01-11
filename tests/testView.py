import unittest

from util.IdentifiedObject import IdentifiedObject
from util.publisher_subscriber.Publisher import Publisher
from tests.mocks.MockControllerForView import MockControllerForView
from src.view.View import View


class ViewTests(unittest.TestCase):

    def test_initialises_empty(self):
        controller = MockControllerForView()
        view = View(controller)

        self.assertEqual(view.get_publisher(), None)
        self.assertEqual(view.get_controller(), controller)

    def test_get_set_controller(self):
        given_controller = MockControllerForView()
        view = View(given_controller)

        registered_controller = view.get_controller()

        self.assertEqual(given_controller, registered_controller)

    def test_get_set_publisher(self):
        view = View(MockControllerForView())
        pub = Publisher()

        view.set_publisher(pub)

        self.assertEqual(pub, view.get_publisher())

    def test_identified_objects_are_passed_to_the_controller(self):
        controller = MockControllerForView()
        view = View(controller)
        detected_object = IdentifiedObject(1, 2, 3, 4, "test")

        view.detect(detected_object)

        self.assertEqual(detected_object, controller.get_given_identified_object())
