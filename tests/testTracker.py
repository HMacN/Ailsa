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

    def test_90_percent_frame_overlap_to_keep_tracking(self):
        tracker = Tracker()
        tracker.set_allowed_absence(2)

        box_1 = Box(0.0, 0.1, 0.0, 0.1, 0.7, "test3")
        box_2 = Box(0.0, 0.11, 0.0, 0.1, 0.7, "test3")

        box_collection_1 = BoundingBoxCollection()
        box_collection_1.add(box_1)

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(box_2)

        tracker.add_new_frame(copy.deepcopy(box_collection_1))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        self.assertEqual(box_collection_2, tracker.get_current_tracks())

