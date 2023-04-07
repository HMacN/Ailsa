import unittest

from util.SafeListEditor import safely_remove_list_indexes as rm
from util.Debugging import debug_print


class SafeListEditorTests(unittest.TestCase):
    def test_removes_list_of_indexes_from_list(self):
        list_to_edit: list = ["A", "B", "C", "D", "E"]
        indices_to_remove: list = [1, 3]

        expected_result: list = ["A", "C", "E"]
        actual_result = rm(list_to_edit, indices_to_remove)

        self.assertEqual(expected_result, actual_result)
