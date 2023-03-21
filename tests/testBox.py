import unittest

from util.Box import Box


class BoxTests(unittest.TestCase):
    def test_to_string_method(self):
        box = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")

        expected_str = "left: 0.2, right: 0.3, lower: 0.2, upper: 0.6, conf: 0.5, label: test1"

        self.assertEqual(expected_str, str(box))
