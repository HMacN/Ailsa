import unittest

from model.Model import Model
from util.BoundingBox import BoundingBox


class ModelTests(unittest.TestCase):

    def test_register_new_detected_objects_and_gets_all_detected_objects(self):
        model = Model()
        item_1 = BoundingBox(1, 1, 2, 2, "test")
        item_2 = BoundingBox(5, 5, 2, 2, "test")
        item_3 = BoundingBox(9, 9, 2, 2, "test")
        items = [item_1, item_2, item_3]

        model.detect(items)
        returned_items = model.get_detected_items()

        self.assertEqual(items, returned_items)
