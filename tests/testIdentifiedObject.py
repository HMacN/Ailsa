import unittest

from util.BoundingBox import BoundingBox


class IdentifiedObjectTests(unittest.TestCase):
    def test_returns_data(self):
        horizontal_distance_to_origin = 16
        vertical_distance_to_origin = 17
        bounding_box_width = 3
        bounding_box_height = 4
        object_name = "Name"

        ident = BoundingBox(horizontal_distance_to_origin,
                            vertical_distance_to_origin,
                            bounding_box_width,
                            bounding_box_height,
                            object_name)

        self.assertEqual(horizontal_distance_to_origin, ident.get_horizontal_distance_to_origin())
        self.assertEqual(vertical_distance_to_origin, ident.get_vertical_distance_to_origin())
        self.assertEqual(bounding_box_width, ident.get_bounding_box_width())
        self.assertEqual(bounding_box_height, ident.get_bounding_box_height())
        self.assertEqual(object_name, ident.get_object_name())

    def test_equality_when_identical_values(self):
        ident_1: BoundingBox = BoundingBox(2, 2, 2, 2, "Test")
        ident_2: BoundingBox = BoundingBox(2, 2, 2, 2, "Test")

        self.assertTrue(ident_1 == ident_2)

    def test_equality_when_same_object(self):
        ident_1: BoundingBox = BoundingBox(2, 2, 2, 2, "Test")
        ident_2 = ident_1

        self.assertTrue(ident_1 == ident_2)

    def test_non_equality_when_different_values(self):
        ident_1: BoundingBox = BoundingBox(2, 2, 2, 2, "Test")
        ident_2: BoundingBox = BoundingBox(1, 2, 2, 2, "Test")
        ident_3: BoundingBox = BoundingBox(2, 1, 2, 2, "Test")
        ident_4: BoundingBox = BoundingBox(2, 2, 1, 2, "Test")
        ident_5: BoundingBox = BoundingBox(2, 2, 2, 1, "Test")
        ident_6: BoundingBox = BoundingBox(2, 2, 2, 2, "Different")
        ident_7: BoundingBox = BoundingBox(1, 1, 1, 1, "Different")

        self.assertTrue(ident_1 != ident_2)
        self.assertTrue(ident_1 != ident_3)
        self.assertTrue(ident_1 != ident_4)
        self.assertTrue(ident_1 != ident_5)
        self.assertTrue(ident_1 != ident_6)
        self.assertTrue(ident_1 != ident_7)
