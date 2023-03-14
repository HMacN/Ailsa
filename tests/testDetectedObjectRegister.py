import unittest

from model.DetectedObjectRegister import DetectedObjectRegister
from util.BoundingBox import BoundingBox


class DetectedObjectRegisterTests(unittest.TestCase):

    def test_can_add_and_retrieve_an_item_by_name(self):
        register = DetectedObjectRegister()
        name = "test"
        item = BoundingBox(1, 1, 1, 1, name)
        list_with_item = [item]

        register.add(item)

        self.assertEqual(list_with_item, register.get_by_name(name))

    def test_can_retrieve_multiple_items_by_name(self):
        register = DetectedObjectRegister()
        name = "test"
        item_1 = BoundingBox(1, 1, 1, 1, name)
        item_2 = BoundingBox(2, 2, 2, 2, name)
        item_3 = BoundingBox(3, 3, 3, 3, name)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items = list()
        items.append(item_1)
        items.append(item_2)
        items.append(item_3)

        self.assertEqual(items, register.get_by_name(name))

    def test_does_not_return_items_with_wrong_name(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        name_2 = "other"
        item_1 = BoundingBox(1, 1, 1, 1, name_1)
        item_2 = BoundingBox(2, 2, 2, 2, name_1)
        item_3 = BoundingBox(3, 3, 3, 3, name_2)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items = list()
        items.append(item_1)
        items.append(item_2)

        self.assertEqual(items, register.get_by_name(name_1))

    def test_register_does_not_allow_duplicates(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 1, 1, name_1)
        item_2 = item_1
        item_3 = BoundingBox(1, 1, 1, 1, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items_given = list()
        items_given.append(item_1)
        items_given.sort()

        items_found = register.get_by_name(name_1)
        items_found.sort()

        self.assertTrue(items_given == items_found)

    def test_register_gets_items_closer_to_horizontal_origin_than_given_value(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items = list()
        items.append(item_1)
        items.append(item_2)

        self.assertEqual(items, register.get_between_horiz_origin_and(8))

    def test_items_closer_to_horizontal_origin_not_returned_if_given_value_overlaps_bounding_box(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items = list()
        items.append(item_1)
        self.assertEqual(items, register.get_between_horiz_origin_and(6))

        items.append(item_2)
        items.sort()
        self.assertEqual(items, register.get_between_horiz_origin_and(7))

    def test_register_gets_items_further_from_horizontal_origin_than_given_value(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items = list()
        items.append(item_2)
        items.append(item_3)

        self.assertEqual(items, register.get_between_horiz_far_edge_and(4))

    def test_items_further_from_horizontal_origin_not_returned_if_given_value_overlaps_bounding_box(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        given_items_1 = list()
        given_items_1.append(item_3)
        returned_items_1 = register.get_between_horiz_far_edge_and(6)
        returned_items_1.sort()

        self.assertEqual(given_items_1, returned_items_1)

        given_items_2 = [item_2, item_3]
        given_items_2.sort()
        returned_items_2 = register.get_between_horiz_far_edge_and(5)
        returned_items_2.sort()

        self.assertEqual(given_items_2, returned_items_2)

    def test_register_gets_items_closer_to_vertical_origin_than_given_value(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items = list()
        items.append(item_1)
        items.append(item_2)

        self.assertEqual(items, register.get_between_vert_origin_and(8))

    def test_items_closer_to_vertical_origin_not_returned_if_given_value_overlaps_bounding_box(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items = list()
        items.append(item_1)
        self.assertEqual(items, register.get_between_vert_origin_and(6))

        items.append(item_2)
        items.sort()
        self.assertEqual(items, register.get_between_vert_origin_and(7))

    def test_register_gets_items_further_from_vertical_origin_than_given_value(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items = list()
        items.append(item_2)
        items.append(item_3)

        self.assertEqual(items, register.get_between_vert_far_edge_and(4))

    def test_items_further_from_vertical_origin_not_returned_if_given_value_overlaps_bounding_box(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        given_items_1 = list()
        given_items_1.append(item_3)
        returned_items_1 = register.get_between_vert_far_edge_and(6)
        returned_items_1.sort()

        self.assertEqual(given_items_1, returned_items_1)

        given_items_2 = [item_2, item_3]
        given_items_2.sort()
        returned_items_2 = register.get_between_vert_far_edge_and(5)
        returned_items_2.sort()

        self.assertEqual(given_items_2, returned_items_2)

    def test_get_all_items(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 1, 2, 2, name_1)
        item_2 = BoundingBox(5, 5, 2, 2, name_1)
        item_3 = BoundingBox(9, 9, 2, 2, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        given_items_1 = [item_1, item_2, item_3]
        returned_items_1 = register.get_all()
        returned_items_1.sort()

        self.assertEqual(given_items_1, returned_items_1)

    def test_get_items_overlapping_horizontally_does_not_return_original_item(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(5, 1, 3, 3, name_1)

        register.add(item_1)

        overlapping = []
        found_overlapping = register.get_horiz_overlapping_for(item_1)

        self.assertEqual(overlapping, found_overlapping)

    def test_get_items_overlapping_horizontally(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(5, 1, 3, 3, name_1)
        item_2 = BoundingBox(1, 1, 3, 3, name_1)
        item_3 = BoundingBox(6, 1, 3, 3, name_1)
        item_4 = BoundingBox(4, 1, 3, 3, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)
        register.add(item_4)

        overlapping = [item_3, item_4]
        found_overlapping = register.get_horiz_overlapping_for(item_1)
        found_overlapping.sort()

        self.assertEqual(overlapping, found_overlapping)

    def test_get_items_overlapping_vertically(self):
        register = DetectedObjectRegister()
        name_1 = "test"
        item_1 = BoundingBox(1, 5, 3, 3, name_1)
        item_2 = BoundingBox(1, 1, 3, 3, name_1)
        item_3 = BoundingBox(1, 6, 3, 3, name_1)
        item_4 = BoundingBox(1, 4, 3, 3, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)
        register.add(item_4)

        overlapping = [item_3, item_4]
        found_overlapping = register.get_vert_overlapping_for(item_1)
        found_overlapping.sort()

        self.assertEqual(overlapping, found_overlapping)
