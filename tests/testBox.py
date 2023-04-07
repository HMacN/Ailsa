import unittest

from util.Box import Box
from util.Debugging import debug_print


def floats_eq_7_dp(float_1: float, float_2: float) -> bool:
    rounded_1 = round(float_1, 7)
    rounded_2 = round(float_2, 7)

    debug_print("rounding: ", rounded_1, ", ", rounded_2)

    return rounded_1 == rounded_2


class BoxTests(unittest.TestCase):
    def test_to_string_method(self):
        box = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")

        expected_str = "left: 0.2, right: 0.3, lower: 0.2, upper: 0.6, conf: 0.5, label: test1"

        self.assertEqual(expected_str, str(box))

    def test_given_byte_strings_converted_to_str(self):
        box = Box(0.2, 0.3, 0.2, 0.6, 0.5, b'test1')

        expected_str = "test1"

        self.assertEqual(expected_str, box.label)

    def test_get_overlap_area_with_identical_box(self):
        box_1 = Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1")
        box_2 = Box(0.0, 0.1, 0.0, 0.1, 0.5, "test2")

        self.assertTrue(floats_eq_7_dp(1.0, box_1.get_overlap(box_2)))

    def test_get_overlap_area_with_non_overlapping_boxes(self):
        box_1 = Box(0.1, 0.2, 0.1, 0.2, 0.5, "test1")
        box_2 = Box(0.0, 0.0999999, 0.1, 0.2, 0.5, "test2")
        box_3 = Box(0.1, 0.2, 0.20000001, 0.3, 0.5, "test3")
        box_4 = Box(0.20000001, 0.3, 0.1, 0.2, 0.5, "test4")
        box_5 = Box(0.1, 0.2, 0.0, 0.0999999, 0.5, "test5")

        self.assertTrue(floats_eq_7_dp(0.0, box_1.get_overlap(box_2)))
        self.assertTrue(floats_eq_7_dp(0.0, box_1.get_overlap(box_3)))
        self.assertTrue(floats_eq_7_dp(0.0, box_1.get_overlap(box_4)))
        self.assertTrue(floats_eq_7_dp(0.0, box_1.get_overlap(box_5)))

    def test_get_overlap_gives_decimal_when_partially_overlapping(self):
        box_1 = Box(0.1, 0.2, 0.1, 0.2, 0.5, "test1")
        box_2 = Box(0.05, 0.15, 0.15, 0.25, 0.5, "test2")

        self.assertTrue(floats_eq_7_dp(0.25, box_1.get_overlap(box_2)))
