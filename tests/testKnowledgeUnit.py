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
        actual_results: list = ku.get_seen_items()

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
        actual_results: list = ku.get_seen_items()

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
        actual_results: list = ku.get_seen_items()

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
