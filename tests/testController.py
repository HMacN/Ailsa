import unittest

from tests.mocks.MockControllerForView import MockControllerForView
from src.controller.Controller import Controller
from tests.mocks.MockView import MockView
from controller.IdentifiedObject import IdentifiedObject


class ControllerTests(unittest.TestCase):
    def test_get_set_view(self):
        given_view = MockView(MockControllerForView())
        controller = Controller()

        controller.set_view(given_view)

        registered_view = controller.get_view()

        self.assertEqual(registered_view, given_view)

    def test_identified_object_returns_data(self):
        horizontal_distance_to_origin = 16
        vertical_distance_to_origin = 17
        bounding_box_width = 3
        bounding_box_height = 4
        object_name = "Name"

        ident = IdentifiedObject(horizontal_distance_to_origin,
                                 vertical_distance_to_origin,
                                 bounding_box_width,
                                 bounding_box_height,
                                 object_name)

        self.assertEqual(horizontal_distance_to_origin, ident.get_horizontal_distance_to_origin())
        self.assertEqual(vertical_distance_to_origin, ident.get_vertical_distance_to_origin())
        self.assertEqual(bounding_box_width, ident.get_bounding_box_width())
        self.assertEqual(bounding_box_height, ident.get_bounding_box_height())
        self.assertEqual(object_name, ident.get_object_name())
