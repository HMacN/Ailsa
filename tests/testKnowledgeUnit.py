import unittest

from model.KnowledgeUnit import KnowledgeUnit
from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box


class KnowledgeUnitTests(unittest.TestCase):
    def test_remembers_all_seen_items(self):
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

    def test_where_did_you_see_items_returns_empty_list_if_items_not_seen(self):
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
        ku = KnowledgeUnit()

        expected_results: list = []
        actual_results: list = ku.get_list_of_seen_items_in_category("test")

        self.assertEqual(expected_results, actual_results)

    def test_describe_location_of_on_other_item(self):    # todo finish this
        ku = KnowledgeUnit()
        ku.set_left_and_right(0.2, 0.8)

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.45, 0.55, 0.45, 0.55, 0.5, "A"))
        frame_1.add(Box(0.45, 0.55, 0.45, 0.55, 0.5, "B"))

        ku.add_frame(frame_1, 1)

        expected_results_left: list = ["A", "B"]
        actual_results_left: list = ku.describe_scene()["left"]
        self.assertEqual(expected_results_left, actual_results_left)
