import unittest

from util.Box import Box
from util.BoundingBoxCollection import BoundingBoxCollection


class BoundingBoxCollectionTests(unittest.TestCase):

    def test_can_add_and_get_one_bounding_box(self):
        box_collection = BoundingBoxCollection()
        given_box = Box(0.2, 0.3, 0.2, 0.3, 0.5, "test")
        box_collection.add(given_box)
        retrieved_box = box_collection.get(0)

        self.assertEqual(given_box, retrieved_box)

    def test_can_add_and_get_multiple_boxes(self):
        box_collection = BoundingBoxCollection()
        box_0 = Box(0.2, 0.3, 0.2, 0.3, 0.5, "test1")
        box_1 = Box(0.1, 0.3, 0.2, 0.3, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.5, "test3")

        box_collection.add(box_0)
        box_collection.add(box_1)
        box_collection.add(box_2)

        self.assertEqual(box_0, box_collection.get(0))
        self.assertEqual(box_1, box_collection.get(1))
        self.assertEqual(box_2, box_collection.get(2))

    def test_boxes_are_sorted_by_confidence(self):
        box_collection = BoundingBoxCollection()
        box_0 = Box(0.2, 0.3, 0.2, 0.3, 0.1, "test1")
        box_1 = Box(0.1, 0.3, 0.2, 0.3, 0.3, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.2, "test3")

        box_collection.add(box_0)
        box_collection.add(box_1)
        box_collection.add(box_2)

        box_collection.sort_by_confidence()

        self.assertEqual(box_1, box_collection.get(0))
        self.assertEqual(box_2, box_collection.get(1))
        self.assertEqual(box_0, box_collection.get(2))

    def test_out_of_range_get_indexes_return_none(self):
        box_collection = BoundingBoxCollection()
        given_box = Box(0.2, 0.3, 0.2, 0.3, 0.5, "test")
        box_collection.add(given_box)
        retrieved_box = box_collection.get(1)

        self.assertEqual(None, retrieved_box)

    def test_trim_boxes_by_confidence(self):
        box_collection = BoundingBoxCollection()
        box_0 = Box(0.2, 0.3, 0.2, 0.3, 0.1, "test1")
        box_1 = Box(0.1, 0.3, 0.2, 0.3, 0.3, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.2, "test3")

        box_collection.add(box_0)
        box_collection.add(box_1)
        box_collection.add(box_2)

        box_collection.trim_by_confidence(0.2)

        self.assertEqual(box_1, box_collection.get(0))
        self.assertEqual(box_2, box_collection.get(1))
        self.assertEqual(None, box_collection.get(2))

    def test_get_size(self):
        box_collection = BoundingBoxCollection()
        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection.add(box_0)
        box_collection.add(box_1)
        box_collection.add(box_2)

        self.assertEqual(3, box_collection.size())

    def test_get_size_when_zero(self):
        box_collection = BoundingBoxCollection()

        self.assertEqual(0, box_collection.size())

    def test_to_string_method(self):
        box_collection = BoundingBoxCollection()
        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection.add(box_0)
        box_collection.add(box_1)
        box_collection.add(box_2)

        expected_str = "Box 0: [" + str(box_0) + "]\n" \
                       "Box 1: [" + str(box_1) + "]\n" \
                       "Box 2: [" + str(box_2) + "]"

        self.assertEqual(expected_str, str(box_collection))

    def test_equality_check(self):
        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        c_1 = BoundingBoxCollection()
        c_2 = BoundingBoxCollection()

        c_1.add(box_0)
        c_1.add(box_1)
        c_1.add(box_2)

        c_2.add(box_0)
        c_2.add(box_1)
        c_2.add(box_2)

        self.assertEqual(c_1, c_2)

    def test_inequality_check(self):
        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")
        box_3 = Box(0.0, 0.4, 0.2, 0.3, 0.7, "test3")

        c_1 = BoundingBoxCollection()
        c_2 = BoundingBoxCollection()

        c_1.add(box_0)
        c_1.add(box_1)
        c_1.add(box_2)

        c_2.add(box_0)
        c_2.add(box_1)
        c_2.add(box_3)

        self.assertNotEqual(c_1, c_2)



