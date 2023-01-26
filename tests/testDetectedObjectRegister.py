import unittest

from model.DetectedObjectRegister import DetectedObjectRegister
from util.IdentifiedObject import IdentifiedObject


class DetectedObjectRegisterTests(unittest.TestCase):

    def test_can_add_and_retrieve_an_item_by_name(self):
        register = DetectedObjectRegister()
        name = "test"
        item = IdentifiedObject(1, 1, 1, 1, name)
        list_with_item = [item]

        register.add(item)

        self.assertEqual(list_with_item, register.get_by_name(name))

    def test_can_retrieve_multiple_items_by_name(self):
        register = DetectedObjectRegister()
        name = "test"
        item_1 = IdentifiedObject(1, 1, 1, 1, name)
        item_2 = IdentifiedObject(2, 2, 2, 2, name)
        item_3 = IdentifiedObject(3, 3, 3, 3, name)

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
        item_1 = IdentifiedObject(1, 1, 1, 1, name_1)
        item_2 = IdentifiedObject(2, 2, 2, 2, name_1)
        item_3 = IdentifiedObject(3, 3, 3, 3, name_2)

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
        item_1 = IdentifiedObject(1, 1, 1, 1, name_1)
        item_2 = item_1
        item_3 = IdentifiedObject(1, 1, 1, 1, name_1)

        register.add(item_1)
        register.add(item_2)
        register.add(item_3)

        items_given = list()
        items_given.append(item_1)
        items_given.sort()

        items_found = register.get_by_name(name_1)
        items_found.sort()

        self.assertTrue(items_given == items_found)
