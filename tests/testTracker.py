import copy
import unittest

from model.Tracker import Tracker
from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box
from util.Debugging import debug_print


class ModelTests(unittest.TestCase):

    def test_track_new_items(self):
        tracker = Tracker()

        box_collection = BoundingBoxCollection()
        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection.add(box_0)
        box_collection.add(box_1)
        box_collection.add(box_2)

        tracker.add_new_frame(copy.deepcopy(box_collection))

        current_tracks = tracker.get_current_tracks()

        self.assertEqual(box_collection, current_tracks,
                         msg=("Given tracks: \n" + str(box_collection) +
                              "\n does not equal tracked boxes: \n" + str(current_tracks)))

    def test_track_existing_items_after_multiple_frame_absence(self):
        tracker = Tracker()
        tracker.set_allowed_absence(6)

        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection_1 = BoundingBoxCollection()
        box_collection_1.add(box_0)
        box_collection_1.add(box_1)
        box_collection_1.add(box_2)

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(box_0)
        box_collection_2.add(box_1)

        tracker.add_new_frame(copy.deepcopy(box_collection_1))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        current_tracks = tracker.get_current_tracks()

        self.assertEqual(box_collection_1, current_tracks,
                         msg=("Expected tracks before absence: \n" + str(box_collection_1) +
                              "\n does not equal tracked items: \n" + str(current_tracks)))

    def test_stop_tracking_items_after_multiple_frame_absence(self):
        tracker = Tracker()
        tracker.set_allowed_absence(6)

        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection_1 = BoundingBoxCollection()
        box_collection_1.add(box_0)
        box_collection_1.add(box_1)
        box_collection_1.add(box_2)

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(box_0)
        box_collection_2.add(box_1)

        tracker.add_new_frame(copy.deepcopy(box_collection_1))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        current_tracks = tracker.get_current_tracks()

        self.assertEqual(box_collection_2, current_tracks,
                         msg=("Expected tracks after absence: \n" + str(box_collection_2) +
                              "\n does not tracked items: \n" + str(current_tracks)))

    def test_set_allowed_frame_absence(self):
        tracker = Tracker()
        tracker.set_allowed_absence(2)

        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection_1 = BoundingBoxCollection()
        box_collection_1.add(box_0)
        box_collection_1.add(box_1)
        box_collection_1.add(box_2)

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(box_0)
        box_collection_2.add(box_1)

        tracker.add_new_frame(copy.deepcopy(box_collection_1))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        self.assertEqual(box_collection_1, tracker.get_current_tracks(),
                         msg=("Expected tracks before allowed absence ends:\n" + str(box_collection_1) +
                              "\n does not equal current tracks: \n" + str(tracker.get_current_tracks())))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        self.assertEqual(box_collection_2, tracker.get_current_tracks(),
                         msg=("Expected tracks after allowed absence ends: \n" + str(box_collection_2) +
                              "\n does not equal current tracks: \n" + str(tracker.get_current_tracks())))

    def test_frame_overlap_to_keep_tracking(self):
        tracker = Tracker()
        tracker.set_allowed_absence(2)

        box_1 = Box(0.0, 0.1, 0.0, 0.1, 0.7, "test3")
        box_2 = Box(0.0, 0.101, 0.0, 0.1, 0.7, "test3")

        box_collection_1 = BoundingBoxCollection()
        box_collection_1.add(box_1)

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(box_2)

        tracker.add_new_frame(copy.deepcopy(box_collection_1))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        self.assertEqual(box_collection_2, tracker.get_current_tracks(),
                         msg="Expected tracks after new frame: \n" + str(box_collection_2) +
                         "\n does not equal current tracks: \n" + str(tracker.get_current_tracks()))

    def test_set_frame_iou_to_keep_tracking(self):
        tracker = Tracker(iou_threshold=0.143)
        tracker.set_allowed_absence(20)

        box_1 = Box(0.0, 0.1, 0.0, 0.1, 0.7, "test3")
        box_2 = Box(0.05, 0.15, 0.05, 0.15, 0.7, "test3")
        box_3 = Box(0.0499, 0.15, 0.05, 0.15, 0.7, "test3")

        frame_1 = BoundingBoxCollection()
        frame_1.add(box_1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(box_2)

        frame_3 = BoundingBoxCollection()
        frame_3.add(box_3)

        tracker.add_new_frame(copy.deepcopy(frame_1))
        tracker.add_new_frame(copy.deepcopy(frame_2))
        tracker.add_new_frame(copy.deepcopy(frame_3))

        expected_result = BoundingBoxCollection()
        expected_result.add(box_3)
        expected_result.add(box_2)
        actual_result = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg="Expected tracks before IoU change: \n" + str(expected_result) +
                         "\n does not equal current tracks: \n" + str(actual_result))


