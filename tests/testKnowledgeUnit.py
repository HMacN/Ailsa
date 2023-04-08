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

        ku.add_frame(frame)

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

        ku.add_frame(frame)

        expected_results: list = ["A", "B", "C"]
        actual_results: list = ku.get_seen_items()

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                         "\ndid not equal the actual value: \n" + str(actual_results))

    def test_remembers_seen_items_across_multiple_frames(self):
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_3)

        expected_results: list = ["A", "B", "C"]
        actual_results: list = ku.get_seen_items()

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                         "\ndid not equal the actual value: \n" + str(actual_results))

    def test_have_you_seen_an_item_returns_1(self):
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_3)

        expected_results: int = 1
        actual_results: int = ku.have_you_seen_a("B")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                         "\ndid not equal the actual value: \n" + str(actual_results))

    def test_have_you_seen_an_item_returns_0(self):
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "A"))
        ku.add_frame(frame_1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "C"))
        ku.add_frame(frame_3)

        expected_results: int = 0
        actual_results: int = ku.have_you_seen_a("D")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                         "\ndid not equal the actual value: \n" + str(actual_results))

    def test_have_you_seen_item_returns_count_of_max_number_seen_at_one_time(self):
        ku = KnowledgeUnit()

        frame_1 = BoundingBoxCollection()
        frame_1.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        frame_2.add(Box(0.0, 0.1, 0.0, 0.1, 0.5, "B"))
        ku.add_frame(frame_2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(Box(0.2, 0.3, 0.2, 0.6, 0.5, "B"))
        ku.add_frame(frame_3)

        expected_results: int = 2
        actual_results: int = ku.have_you_seen_a("B")

        self.assertEqual(expected_results, actual_results,
                         msg="The expected value: \n" + str(expected_results) +
                         "\ndid not equal the actual value: \n" + str(actual_results))


