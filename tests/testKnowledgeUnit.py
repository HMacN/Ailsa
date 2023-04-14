import unittest

from model.KnowledgeUnit import KnowledgeUnit
from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box


class KnowledgeUnitTests(unittest.TestCase):
    def test_remembers_all_seen_items(self):
        """
        Test that the unit remembers what item types it's seen.
        @return:
        """
        ku = KnowledgeUnit()

        frame = BoundingBoxCollection()
        frame.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1"))
        frame.add(Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2"))
        frame.add(Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3"))

        ku.add_frame(frame, 1)

        expected_results: list = ["test1", "test2", "test3"]
        actual_results: list = ku.get_list_of_all_seen_items()

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_returns_seen_items_in_alphabetical_order(self):
        """
        Test that the items returned are in alphabetical order.

        @return:
        """
        ku = KnowledgeUnit()

        frame = BoundingBoxCollection()
        frame.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        frame.add(Box(0.1, 0.4, 0.1, 0.6, 0.5, "C"))
        frame.add(Box(0.0, 0.3, 0.2, 0.3, 0.7, "B"))

        ku.add_frame(frame, 1)

        expected_results: list = ["A", "B", "C"]
        actual_results: list = ku.get_list_of_all_seen_items()

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_remembers_seen_items_across_multiple_frames(self):
        """
        Test that the memory of items persists across multiple frames.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1, 1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_2, 2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_3, 3)

        expected_results: list = ["A", "B", "C"]
        actual_results: list = ku.get_list_of_all_seen_items()

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_have_you_seen_an_item_returns_1(self):
        """
        Test that, having seen an item, the unit returns a value of one.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1, 1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_2, 2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_3, 3)

        expected_results: int = 1
        actual_results: int = ku.how_many_have_you_seen("B")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_have_you_seen_an_item_returns_0(self):
        """
        Test that have you seen an item returns zero if the item has not been seen.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1, 1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_2, 2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_3, 3)

        expected_results: int = 0
        actual_results: int = ku.how_many_have_you_seen("D")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_have_you_seen_item_returns_count_of_max_number_seen_at_one_time(self):
        """
        Test that have you seen an item returns the maximum number seen at one time, rather than a count of the total
        number seen.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_1, 1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        frame_2.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_2, 2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_3, 3)

        expected_results: int = 2
        actual_results: int = ku.how_many_have_you_seen("B")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_when_did_you_see_returns_empty_list_if_not_seen(self):
        """
        test that an empty list of times seen is returned if an item has nto actually been seen.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1, 1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_2, 2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_3, 3)

        expected_results: list = list()
        actual_results: list = ku.when_did_you_see("D")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_when_did_you_see_returns_time_last_seen(self):
        """
        Test that a correct list of times is returned from this function.  Each time should correspond to the frame that
        an object was last seen on a particular sighting.


        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1, 2)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_2, 3)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_3, 4)

        frame_4 = BoundingBoxCollection()
        frame_4.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_4, 5)

        expected_results: list = [4]
        actual_results: list = ku.when_did_you_see("B")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_when_did_you_see_returns_times_item_seen(self):
        """
        Test that a correct list of times is returned from this function.  Each time should correspond to the frame that
        an object was last seen on a particular sighting.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1, 2)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_2, 3)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_3, 4)

        frame_4 = BoundingBoxCollection()
        frame_4.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_4, 5)

        frame_5 = BoundingBoxCollection()
        frame_5.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_5, 6)

        frame_6 = BoundingBoxCollection()
        frame_6.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_6, 7)

        frame_7 = BoundingBoxCollection()
        frame_7.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_7, 8)

        expected_results: list = [5, 8]
        actual_results: list = ku.when_did_you_see("B")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_when_did_you_see_items_times_item_seen_copes_with_frames_at_irregular_time_steps(self):
        """
        Test that the function is not thrown off by frames coming in at irregular intervals.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1, 1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_2, 2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_3, 8)

        frame_4 = BoundingBoxCollection()
        frame_4.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_4, 10)

        frame_5 = BoundingBoxCollection()
        frame_5.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_5, 16)

        frame_6 = BoundingBoxCollection()
        frame_6.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_6, 18)

        frame_7 = BoundingBoxCollection()
        frame_7.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_7, 20)

        expected_results: list = [10, 20]
        actual_results: list = ku.when_did_you_see("B")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_where_did_you_see_items_returns_empty_list_if_items_not_seen(self):
        """
        Test that this function returns an empty list of locations if an object hasn't been seen.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "A"))
        ku.add_frame(frame_1, 2)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.2, 0.3, 0.3, 0.5, "B"))
        ku.add_frame(frame_2, 3)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.3, 0.3, 0.4, 0.4, 0.5, "C"))
        ku.add_frame(frame_3, 4)

        expected_results: list = list()
        actual_results: list = ku.where_did_you_see("D")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_where_item_returns_empty_str_for_lone_object(self):
        """
        Test that this function returns an empty string for objects that have no special categories.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "A"))
        ku.add_frame(frame_1, 2)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.2, 0.3, 0.3, 0.5, "B"))
        ku.add_frame(frame_2, 3)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.3, 0.3, 0.4, 0.4, 0.5, "C"))
        ku.add_frame(frame_3, 4)

        expected_results: list = [""]
        actual_results: list = ku.where_did_you_see("B")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_where_item_returns_on_floor_if_item_not_normally_on_floor(self):
        """
        Test that objects that are not usually on the floor are mentioned as being on the floor if they are not on top
        of something.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_items_not_normally_on_floor(["A"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "A"))
        ku.add_frame(frame_1, 2)

        expected_results: list = ["on the floor"]
        actual_results: list = ku.where_did_you_see("A")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_where_item_returns_on_floor_for_multiple_items(self):
        """
        Test that the function can handle being called when multiple items of the ame type have been seen.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_items_not_normally_on_floor(["A", "B"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "A"))
        ku.add_frame(frame_1, 2)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.2, 0.3, 0.3, 0.5, "B"))
        ku.add_frame(frame_2, 3)

        expected_results: list = ["on the floor"]
        actual_results: list = ku.where_did_you_see("A")
        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

        expected_results: list = ["on the floor"]
        actual_results: list = ku.where_did_you_see("B")
        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_renames_impossible_items(self):
        """
        Test that any items which have been listed as not possible in the area have been renamed.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_impossible_items(["A"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "A"))
        ku.add_frame(frame_1, 2)

        expected_results: list = list(["unknown item"])
        actual_results: list = ku.get_list_of_all_seen_items()
        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_describe_scene_object_centre(self):
        """
        Test that any items directly ahead have their location properly described.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.45, 0.55, 0.45, 0.55, 0.5, "A"))
        ku.add_frame(frame_1, 1)

        expected_results: list = ["A"]
        actual_results: dict = ku.describe_scene()["ahead"]
        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_describe_scene_object_centre_left_and_right_boundaries_default_values(self):
        """
        Test that any items which are near the boundaries of being on the left, and right, sides of the frame have
        their locations correctly described.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.00, 0.32, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.00, 0.34, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.67, 1.00, 0.45, 0.55, 0.5, "C"))
        frame_1.add(Box(0.65, 1.00, 0.45, 0.55, 0.5, "D"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["B", "D"]
        actual_results: dict = ku.describe_scene()["ahead"]
        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_describe_scene_multiple_objects_of_same_type(self):
        """
        Test that the function can handle multiple items of the same type in scene.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.45, 0.55, 0.1, 0.3, 0.5, "A"))
        frame_1.add(Box(0.45, 0.55, 0.3, 0.4, 0.5, "A"))
        frame_1.add(Box(0.45, 0.55, 0.4, 0.5, 0.5, "A"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["A", "A", "A"]
        actual_results: dict = ku.describe_scene()["ahead"]
        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_describe_scene_objects_left(self):
        """
        Test that any items to the left have their location properly described.


        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.00, 0.30, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.00, 0.32, 0.45, 0.55, 0.5, "B"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["A", "B"]
        actual_results: dict = ku.describe_scene()["left"]
        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_describe_scene_objects_right(self):
        """
        Test that any items to the right have their location properly described.


        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.67, 0.99, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.70, 0.99, 0.45, 0.55, 0.5, "B"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["A", "B"]
        actual_results: dict = ku.describe_scene()["right"]
        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                             "\ndid not equal the actual value: \n" + str(actual_results))

    def test_describe_large_objects_left_ahead_right(self):
        """
        Test that items that stretch across the left and right boundaries have their  have their location properly
        described.


        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.10, 0.40, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.10, 0.90, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.60, 0.90, 0.45, 0.55, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results_left: list = ["A", "B"]
        actual_results_left: list = ku.describe_scene()["left"]
        self.assertEqual(expected_results_left, actual_results_left)

        expected_results_ahead: list = ["A", "B", "C"]
        actual_results_ahead: list = ku.describe_scene()["ahead"]
        self.assertEqual(expected_results_ahead, actual_results_ahead)

        expected_results_right: list = ["B", "C"]
        actual_results_right: list = ku.describe_scene()["right"]
        self.assertEqual(expected_results_right, actual_results_right)

    def test_set_left_and_right_cut_offs(self):
        """
        Test that the left and right cut-off lines can be adjusted.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_left_and_right(0.2, 0.8)

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.10, 0.19, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.10, 0.21, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.10, 0.90, 0.45, 0.55, 0.5, "C"))
        frame_1.add(Box(0.79, 0.90, 0.45, 0.55, 0.5, "D"))
        frame_1.add(Box(0.81, 0.90, 0.45, 0.55, 0.5, "E"))

        ku.add_frame(frame_1, 1)

        expected_results_left: list = ["A", "B", "C"]
        actual_results_left: list = ku.describe_scene()["left"]
        self.assertEqual(expected_results_left, actual_results_left)

        expected_results_ahead: list = ["B", "C", "D"]
        actual_results_ahead: list = ku.describe_scene()["ahead"]
        self.assertEqual(expected_results_ahead, actual_results_ahead)

        expected_results_right: list = ["C", "D", "E"]
        actual_results_right: list = ku.describe_scene()["right"]
        self.assertEqual(expected_results_right, actual_results_right)

    def test_custom_category_items_mentioned_in_describe_scene(self):
        """
        Test that items in a custom category are described as such in the describe scene function.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_custom_category("test", ["A"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.10, 0.19, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.10, 0.21, 0.45, 0.55, 0.5, "B"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["A"]
        actual_results: list = ku.describe_scene()["test"]
        self.assertEqual(expected_results, actual_results)

    def test_custom_category_multiple_items_mentioned_in_describe_scene(self):
        """
        Test that the describe scene function copes with multiple instances of custom category item types.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_custom_category("test", ["A", "C", "E"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.10, 0.19, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.10, 0.21, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.10, 0.90, 0.45, 0.55, 0.5, "C"))
        frame_1.add(Box(0.79, 0.90, 0.45, 0.55, 0.5, "D"))
        frame_1.add(Box(0.81, 0.90, 0.45, 0.55, 0.5, "E"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["A", "C", "E"]
        actual_results: list = ku.describe_scene()["test"]
        self.assertEqual(expected_results, actual_results)

    def test_custom_category_duplicate_items_mentioned_in_describe_scene(self):
        """
        Test that the describe scene function copes with multiple instances of a single category item type.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_custom_category("test", ["A", "C"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.10, 0.19, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.10, 0.21, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.10, 0.90, 0.45, 0.55, 0.5, "C"))
        frame_1.add(Box(0.79, 0.90, 0.45, 0.55, 0.5, "C"))
        frame_1.add(Box(0.81, 0.90, 0.45, 0.55, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["A", "C", "C", "C"]
        actual_results: list = ku.describe_scene()["test"]
        self.assertEqual(expected_results, actual_results)

    def test_multiple_custom_category_items_mentioned_in_describe_scene(self):
        """
        Test that the describe scene function copes with multiple custom categories.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_custom_category("test", ["A", "B"])
        ku.set_custom_category("test2", ["A", "C"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.10, 0.19, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.10, 0.21, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.10, 0.90, 0.45, 0.55, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["A", "B"]
        actual_results: list = ku.describe_scene()["test"]
        self.assertEqual(expected_results, actual_results)

        expected_results: list = ["A", "C"]
        actual_results: list = ku.describe_scene()["test2"]
        self.assertEqual(expected_results, actual_results)

    def test_get_all_seen_items_in_category(self):
        """
        Test can get all items seen in a custom category.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_custom_category("test", ["A", "C"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1, 1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_2, 2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_3, 3)

        expected_results: list = ["A", "C"]
        actual_results: list = ku.get_list_of_seen_items_in_category("test")

        self.assertEqual(expected_results, actual_results)

    def test_get_all_seen_items_in_category_returns_empty_list_on_invalid_category(self):
        """
        Test that an invalid category name produces an empty list, instead of throwing an error.

        @return:
        """
        ku = KnowledgeUnit()

        expected_results: list = []
        actual_results: list = ku.get_list_of_seen_items_in_category("test")

        self.assertEqual(expected_results, actual_results)

    def test_where_is_unseen_item(self):
        """
        Test that the where is function returns an empty dict if an item has not been seen.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()

        ku.add_frame(frame_1, 1)

        expected_results: dict = {}
        actual_results: dict = ku.where_is("A")
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_ahead(self):
        """
        Test that an item directly ahead is given the correct direction in the where is function.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["ahead"]
        actual_results: dict = ku.where_is("A")["direction"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_left_ahead_right(self):
        """
        Test that items in various directions are given the correct directions in the where is function.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.10, 0.32, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.10, 0.34, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.10, 0.90, 0.45, 0.55, 0.5, "C"))
        frame_1.add(Box(0.65, 0.90, 0.45, 0.55, 0.5, "D"))
        frame_1.add(Box(0.67, 0.90, 0.45, 0.55, 0.5, "E"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["left"]
        actual_results: dict = ku.where_is("A")["direction"]
        self.assertEqual(expected_results, actual_results)

        expected_results: list = ["ahead", "left"]
        actual_results: dict = ku.where_is("B")["direction"]
        self.assertEqual(expected_results, actual_results)

        expected_results: list = ["ahead", "left", "right"]
        actual_results: dict = ku.where_is("C")["direction"]
        self.assertEqual(expected_results, actual_results)

        expected_results: list = ["ahead", "right"]
        actual_results: dict = ku.where_is("D")["direction"]
        self.assertEqual(expected_results, actual_results)

        expected_results: list = ["right"]
        actual_results: dict = ku.where_is("E")["direction"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_beneath_gives_empty_list_if_not_beneath_anything(self):
        """
        Test the where is function returns an empty list for "beneath" if there are no wall and ceiling items above the
        target.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))

        ku.add_frame(frame_1, 1)

        expected_results: list = []
        actual_results: dict = ku.where_is("A")["beneath"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_beneath_wall_object(self):
        """
        Test the where is function returns an empty list for "beneath" if there are no wall and ceiling items above the
        target.

        @return:
        """
        ku = KnowledgeUnit()
        ku.add_wall_and_ceiling_objects(["B"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))
        frame_1.add(Box(0.40, 0.60, 0.70, 0.80, 0.5, "B"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["B"]
        actual_results: dict = ku.where_is("A")["beneath"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_beneath_wall_object_not_above_bottom_line(self):
        """
        Test items are only listed as being beneath something if their bottom edge is below the bottom edge of the wall
        or ceiling object.

        @return:
        """
        ku = KnowledgeUnit()
        ku.add_wall_and_ceiling_objects(["B", "C"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))
        frame_1.add(Box(0.40, 0.60, 0.51, 0.80, 0.5, "B"))
        frame_1.add(Box(0.40, 0.60, 0.49, 0.80, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["B"]
        actual_results: dict = ku.where_is("A")["beneath"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_beneath_wall_object_only_if_directly_beneath(self):
        """
        Test items are only listed as being beneath something if they are actually beneath it.  Defined as having at
        least some vertical overlap.

        @return:
        """
        ku = KnowledgeUnit()
        ku.add_wall_and_ceiling_objects(["B", "C", "D", "E", "F"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.33, 0.66, 0.10, 0.20, 0.5, "A"))

        frame_1.add(Box(0.10, 0.32, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.10, 0.34, 0.45, 0.55, 0.5, "C"))
        frame_1.add(Box(0.10, 0.90, 0.45, 0.55, 0.5, "D"))
        frame_1.add(Box(0.65, 0.90, 0.45, 0.55, 0.5, "E"))
        frame_1.add(Box(0.67, 0.90, 0.45, 0.55, 0.5, "F"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["C", "D", "E"]
        actual_results: dict = ku.where_is("A")["beneath"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_on_top_of_returns_empty_str_if_not_on_top_of_other_object(self):
        """
        Test that if the item is not on top of anything, that the item it is on top of is listed as an empty string.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))

        ku.add_frame(frame_1, 1)

        expected_results: str = ""
        actual_results: dict = ku.where_is("A")["on top of"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_on_top_of_other_object(self):
        """
        Test that if an item is on top of another item then it is listed appropriately.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))
        frame_1.add(Box(0.40, 0.60, 0.40, 0.51, 0.5, "B"))

        ku.add_frame(frame_1, 1)

        expected_results: str = "B"
        actual_results: dict = ku.where_is("A")["on top of"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_on_top_of_multiple_objects_gives_largest_area_below(self):
        """
        Test that the item a target item is on top of is the one that has the largest area below the lower edge of the
        target item.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))
        frame_1.add(Box(0.40, 0.60, 0.40, 0.71, 0.5, "B"))
        frame_1.add(Box(0.40, 0.60, 0.30, 0.51, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results: str = "C"
        actual_results: dict = ku.where_is("A")["on top of"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_on_top_of_other_object_only_when_directly_above(self):
        """
        Test that for a target item to be listed as on top of another item, it must have at least some horizontal
        overlap.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.33, 0.66, 0.10, 0.50, 0.5, "A"))

        frame_1.add(Box(0.10, 0.32, 0.45, 0.55, 0.5, "B"))
        frame_1.add(Box(0.10, 0.34, 0.45, 0.55, 0.5, "C"))
        frame_1.add(Box(0.10, 0.90, 0.45, 0.55, 0.5, "D"))
        frame_1.add(Box(0.65, 0.90, 0.45, 0.55, 0.5, "E"))
        frame_1.add(Box(0.67, 0.90, 0.45, 0.55, 0.5, "F"))

        ku.add_frame(frame_1, 1)

        expected_on_top: str = "A"
        not_expected_on_top: str = ""

        actual_results: dict = ku.where_is("B")["on top of"]
        self.assertEqual(not_expected_on_top, actual_results)

        actual_results: dict = ku.where_is("C")["on top of"]
        self.assertEqual(expected_on_top, actual_results)

        actual_results: dict = ku.where_is("D")["on top of"]
        self.assertEqual(expected_on_top, actual_results)

        actual_results: dict = ku.where_is("E")["on top of"]
        self.assertEqual(expected_on_top, actual_results)

        actual_results: dict = ku.where_is("F")["on top of"]
        self.assertEqual(not_expected_on_top, actual_results)

    def test_where_is_item_on_top_of_other_object_must_overlap(self):
        """
        Test that a target item will not be listed as on top of another item unless it overlaps.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))
        frame_1.add(Box(0.40, 0.60, 0.31, 0.51, 0.5, "B"))
        frame_1.add(Box(0.40, 0.60, 0.28, 0.49, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results: str = "B"
        actual_results: dict = ku.where_is("A")["on top of"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_on_top_of_other_object_does_not_give_furniture_on_top_of_items(self):
        """
        Test that any items listed as being furniture are not listed as being on top of other items.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_furniture_items(["A"])

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))
        frame_1.add(Box(0.40, 0.60, 0.30, 0.55, 0.5, "B"))
        frame_1.add(Box(0.40, 0.60, 0.40, 0.55, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results: str = ""
        actual_results: dict = ku.where_is("A")["on top of"]
        self.assertEqual(expected_results, actual_results)

    def test_where_is_item_on_top_of_other_object_set_max_gap(self):
        """
        Test that the maximum vertical gap between items before being listed as being on top of the other is adjustable.

        @return:
        """
        ku = KnowledgeUnit()
        ku.set_max_gap_for_item_on_top_of_another_item(0.1)

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))
        frame_1.add(Box(0.40, 0.60, 0.31, 0.41, 0.5, "B"))
        frame_1.add(Box(0.40, 0.60, 0.20, 0.39, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results: str = "B"
        actual_results: dict = ku.where_is("A")["on top of"]
        self.assertEqual(expected_results, actual_results)

    def test_get_items_in_between_user_and_item_gives_empty_list_when_item_not_seen(self):
        """
        Test get items between user and target item does not list any items if there aren't any.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()

        ku.add_frame(frame_1, 1)

        expected_results: list = []
        actual_results: list = ku.items_between_user_and("A")
        self.assertEqual(expected_results, actual_results)

    def test_get_items_in_between_user_and_item_gives_list_of_all_items_below_target(self):
        """
        Test get items between user and target item lists all items which may be inbetween the user and the target item.

        @return:
        """
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.40, 0.60, 0.50, 0.60, 0.5, "A"))
        frame_1.add(Box(0.10, 0.20, 0.10, 0.20, 0.5, "B"))
        frame_1.add(Box(0.20, 0.80, 0.40, 0.55, 0.5, "C"))

        ku.add_frame(frame_1, 1)

        expected_results: list = ["B", "C"]
        actual_results: list = ku.items_between_user_and("A")
        self.assertEqual(expected_results, actual_results)
