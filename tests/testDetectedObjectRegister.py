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
