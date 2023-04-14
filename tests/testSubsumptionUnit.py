import copy
import unittest

from model.SubsumptionUnit import SubsumptionUnit
from util.BoxList import BoxList
from util.Box import Box


class MyTestCase(unittest.TestCase):
    def test_subsumes_bboxes_to_first_value_on_subsumption_list_(self):
        """
        Test that the unit subsumes items into the correct type.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.001, 0.099, 0.001, 0.099, 0.5, "test2"))

        subsumption_list: list = ["test1", "test2"]

        su.add_list(subsumption_list)

        expected_result = BoxList()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_does_not_subsume_bboxes_that_are_not_overlapping(self):
        """
        Test that the unit does not subsume items that are not overlapping.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.2, 0.35, 0.2, 0.3, 0.5, "test2"))

        subsumption_list: list = ["test1", "test2"]

        su.add_list(subsumption_list)

        expected_result = BoxList()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        expected_result.add(Box(0.2, 0.35, 0.2, 0.3, 0.5, "test2"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_can_subsume_multiple_items(self):
        """
        Test that the unit can subsume multiple items into each other.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.0, 0.05, 0.0, 0.1, 0.5, "test2"))
        given_box_collection.add(Box(0.05, 0.1, 0.0, 0.1, 0.5, "test3"))

        subsumption_list: list = ["test1", "test2", "test3"]

        su.add_list(subsumption_list)

        expected_result = BoxList()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_can_handle_multiple_subsumption_lists(self):
        """
        Test that the unit can handle multiple lists of possible items to subsume.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.0, 0.05, 0.0, 0.1, 0.5, "test2"))

        given_box_collection.add(Box(0.3, 0.4, 0.3, 0.4, 0.5, "test3"))
        given_box_collection.add(Box(0.35, 0.4, 0.3, 0.4, 0.5, "test4"))

        subsumption_list_1: list = ["test1", "test2"]
        subsumption_list_2: list = ["test3", "test4"]

        su.add_list(subsumption_list_1)
        su.add_list(subsumption_list_2)

        expected_result = BoxList()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        expected_result.add(Box(0.3, 0.4, 0.3, 0.4, 0.5, "test3"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_can_handle_multiple_nested_bboxes(self):
        """
        Test that nested items are subsumed properly.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.00, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.01, 0.1, 0.0, 0.1, 0.5, "test2"))
        given_box_collection.add(Box(0.02, 0.1, 0.0, 0.1, 0.5, "test2"))
        given_box_collection.add(Box(0.03, 0.1, 0.0, 0.1, 0.5, "test2"))

        subsumption_list_1: list = ["test1", "test2"]

        su.add_list(subsumption_list_1)

        expected_result = BoxList()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_chain_of_subsume_ops(self):
        """
        Test items are subsumed correctly, even if the item they are subsumed into is also subsumed.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.00, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.01, 0.1, 0.0, 0.1, 0.5, "test2"))
        given_box_collection.add(Box(0.02, 0.1, 0.0, 0.1, 0.5, "test3"))
        given_box_collection.add(Box(0.03, 0.1, 0.0, 0.1, 0.5, "test4"))

        subsumption_list_1: list = ["test1", "test2"]
        subsumption_list_2: list = ["test2", "test3"]
        subsumption_list_3: list = ["test3", "test4"]

        su.add_list(subsumption_list_1)
        su.add_list(subsumption_list_2)
        su.add_list(subsumption_list_3)

        expected_result = BoxList()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_chain_of_subsume_ops_order_does_not_matter(self):
        """
        Test that the order the items are subsumed in does not matter.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.03, 0.1, 0.0, 0.1, 0.5, "test4"))
        given_box_collection.add(Box(0.00, 0.1, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.02, 0.1, 0.0, 0.1, 0.5, "test3"))
        given_box_collection.add(Box(0.01, 0.1, 0.0, 0.1, 0.5, "test2"))

        subsumption_list_3: list = ["test3", "test4"]
        subsumption_list_1: list = ["test1", "test2"]
        subsumption_list_2: list = ["test2", "test3"]

        su.add_list(subsumption_list_1)
        su.add_list(subsumption_list_2)
        su.add_list(subsumption_list_3)

        expected_result = BoxList()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))
        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_set_overlap_threshold(self):
        """
        Test that the amount an item must be overlapping another by to be subsumed can be set.

        @return:
        """
        su = SubsumptionUnit()
        su.set_overlap_threshold(0.5)

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.0000, 0.1000, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.0499, 0.1499, 0.0, 0.1, 0.5, "test2"))
        given_box_collection.add(Box(0.0501, 0.1501, 0.0, 0.1, 0.5, "test3"))

        subsumption_list_1: list = ["test1", "test2", "test3"]

        su.add_list(subsumption_list_1)

        expected_result = BoxList()
        expected_result.add(Box(0.0000, 0.1000, 0.0, 0.1, 0.5, "test1"))
        expected_result.add(Box(0.0501, 0.1501, 0.0, 0.1, 0.5, "test3"))

        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_subsumes_items_of_same_type_automatically(self):
        """
        Test that, even without a dedicated list of item to subsume, items are subsumed into items of their own type.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.0000, 0.1000, 0.0, 0.1, 0.5, "test1"))
        given_box_collection.add(Box(0.0001, 0.0999, 0.0, 0.1, 0.5, "test1"))

        expected_result = BoxList()
        expected_result.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1"))

        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

    def test_items_of_same_type_subsume_into_largest_box(self):
        """
        Test that items of the same type subsume into the largest bounding box by area.

        @return:
        """
        su = SubsumptionUnit()

        given_box_collection = BoxList()
        given_box_collection.add(Box(0.00, 0.90, 0.00, 0.90, 0.5, "test1"))
        given_box_collection.add(Box(0.00, 0.10, 0.00, 0.10, 0.5, "test1"))
        given_box_collection.add(Box(0.01, 0.09, 0.01, 0.09, 0.5, "test1"))
        given_box_collection.add(Box(0.30, 0.60, 0.30, 0.60, 0.5, "test1"))
        given_box_collection.add(Box(0.40, 0.50, 0.40, 0.50, 0.5, "test1"))

        expected_result = BoxList()
        expected_result.add(Box(0.00, 0.90, 0.00, 0.90, 0.5, "test1"))

        actual_result = su.subsume_bboxes(copy.deepcopy(given_box_collection))

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks: \n" + str(expected_result) +
                              "\n does not equal actual tracks: \n" + str(actual_result)))

