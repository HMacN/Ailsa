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


