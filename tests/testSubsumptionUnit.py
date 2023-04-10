import copy
import unittest

from model.SubsumptionUnit import SubsumptionUnit
from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box


class MyTestCase(unittest.TestCase):
    def test_subsumes_bboxes_to_first_value_on_subsumption_list_(self):
        su = SubsumptionUnit()

        given_box_collection = BoundingBoxCollection()
        given_box_collection.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.001, 0.099, 0.001, 0.099, 0.5, "test2"))

        subsumption_list: list = ["test1", "test2"]

        su.add_list(subsumption_list)

        expected_result = BoundingBoxCollection()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_does_not_subsume_bboxes_that_are_not_overlapping(self):
        su = SubsumptionUnit()

        given_box_collection = BoundingBoxCollection()
        given_box_collection.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.2, 0.3, 0.2, 0.3, 0.5, "test2"))

        subsumption_list: list = ["test1", "test2"]

        su.add_list(subsumption_list)

        expected_result = BoundingBoxCollection()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        expected_result.add(Box(0.2, 0.3, 0.2, 0.3, 0.5, "test2"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))
