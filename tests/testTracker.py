import copy
import unittest

from model.Tracker import Tracker
from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box


class TrackerTests(unittest.TestCase):

    def test_track_new_items(self):
        """
        Test that the tracker starts new tracks for new items.

        @return:
        """
        tracker = Tracker()

        box_collection = BoundingBoxCollection()
        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection.add(box_0)
        box_collection.add(box_1)
        box_collection.add(box_2)

        tracker.add_new_frame(copy.deepcopy(box_collection))

        current_tracks, _ = tracker.get_current_tracks()

        self.assertEqual(box_collection, current_tracks,
                         msg=("Given tracks: \n" + str(box_collection) +
                              "\n does not equal tracked boxes: \n" + str(current_tracks)))

    def test_track_existing_items_after_multiple_frame_absence(self):
        """
        Test that the tracker continues to track items after an absence of several frames.

        @return:
        """
        tracker = Tracker(allowed_absence=6)

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

        current_tracks, _ = tracker.get_current_tracks()

        self.assertEqual(box_collection_1, current_tracks,
                         msg=("Expected tracks before absence: \n" + str(box_collection_1) +
                              "\n does not equal tracked items: \n" + str(current_tracks)))

    def test_stop_tracking_items_after_multiple_frame_absence(self):
        """
        Test that the tracker stops tracking items after a suitable number of frames has elapsed.

        @return:
        """
        tracker = Tracker(allowed_absence=6)

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

        current_tracks, _ = tracker.get_current_tracks()

        self.assertEqual(box_collection_2, current_tracks,
                         msg=("Expected tracks after absence: \n" + str(box_collection_2) +
                              "\n does not equal tracked items: \n" + str(current_tracks)))

    def test_set_allowed_frame_absence(self):
        """
        Test that the number of frames an item can be absent for is adjustable.

        @return:
        """
        tracker = Tracker(allowed_absence=2)

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

        expected_result = box_collection_1
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks before allowed absence ends:\n" + str(expected_result) +
                              "\n does not equal current tracks: \n" + str(actual_result)))

        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        expected_result = box_collection_2
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks after allowed absence ends: \n" + str(expected_result) +
                              "\n does not equal current tracks: \n" + str(actual_result)))

    def test_frame_overlap_to_keep_tracking(self):
        """
        Test that the tracker will continue to track item which overlap with their previously recorded bounding box.

        @return:
        """
        tracker = Tracker(allowed_absence=2)

        box_1 = Box(0.0, 0.1, 0.0, 0.1, 0.7, "test3")
        box_2 = Box(0.0, 0.101, 0.0, 0.1, 0.7, "test3")

        box_collection_1 = BoundingBoxCollection()
        box_collection_1.add(box_1)

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(box_2)

        tracker.add_new_frame(copy.deepcopy(box_collection_1))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        expected_result = box_collection_2
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg="Expected tracks after new frame: \n" + str(expected_result) +
                             "\n does not equal current tracks: \n" + str(actual_result))

    def test_keep_tracking_for_appropriate_iou(self):
        """
        Test that the tracker keeps tracking an item if its new bounding box has a high enough IoU with the old one.

        @return:
        """
        tracker = Tracker(iou_threshold=0.143, allowed_absence=20)

        box_1 = Box(0.0, 0.1, 0.0, 0.1, 0.7, "test3")
        box_2 = Box(0.0499, 0.15, 0.05, 0.15, 0.7, "test3")

        frame_1 = BoundingBoxCollection()
        frame_1.add(box_1)

        frame_2 = BoundingBoxCollection()
        frame_2.add(box_2)

        tracker.add_new_frame(copy.deepcopy(frame_1))
        tracker.add_new_frame(copy.deepcopy(frame_2))

        expected_result = BoundingBoxCollection()
        expected_result.add(box_2)
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg="Expected tracks with given IoU: \n" + str(expected_result) +
                             "\n does not equal current tracks: \n" + str(actual_result))

    def test_stops_tracking_for_appropriate_iou(self):
        """
        Test that the tracker stops tracking an item if its new bounding box does not have a high enough IoU with the
        old one.

        @return:
        """
        tracker = Tracker(iou_threshold=0.143, allowed_absence=20)

        box_1 = Box(0.05, 0.15, 0.05, 0.15, 0.7, "test3")
        box_2 = Box(0.0499, 0.15, 0.05, 0.15, 0.7, "test3")
        box_3 = Box(0.0, 0.1, 0.0, 0.999, 0.7, "test3")

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
        expected_result.add(box_2)
        expected_result.add(box_3)
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg="Expected tracks with given IoU: \n" + str(expected_result) +
                             "\n does not equal current tracks: \n" + str(actual_result))

    def test_does_not_return_track_if_below_min_frames(self):
        """
        Test that the tracker does not report tracks that have not been observed for a set number of frames.

        @return:
        """
        tracker = Tracker(min_frames=5)

        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")

        box_collection = BoundingBoxCollection()
        box_collection.add(box_1)

        tracker.add_new_frame(copy.deepcopy(box_collection))
        tracker.add_new_frame(copy.deepcopy(box_collection))
        tracker.add_new_frame(copy.deepcopy(box_collection))
        tracker.add_new_frame(copy.deepcopy(box_collection))

        expected_result = BoundingBoxCollection()
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks before minimum frames: \n" + str(expected_result) +
                              "\n does not equal tracked items: \n" + str(actual_result)))

    def test_returns_track_after_min_frames(self):
        """
        Test that the tracker does report tracks after the minimum number of frames has elapsed.

        @return:
        """
        tracker = Tracker(min_frames=5)

        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")

        box_collection = BoundingBoxCollection()
        box_collection.add(box_1)

        tracker.add_new_frame(copy.deepcopy(box_collection))
        tracker.add_new_frame(copy.deepcopy(box_collection))
        tracker.add_new_frame(copy.deepcopy(box_collection))
        tracker.add_new_frame(copy.deepcopy(box_collection))
        tracker.add_new_frame(copy.deepcopy(box_collection))

        expected_result = box_collection
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks after minimum frames: \n" + str(expected_result) +
                              "\n does not equal tracked items: \n" + str(actual_result)))

    def test_returns_most_likely_object_classification(self):
        """
        Test that the tracker returns the item classification associated with the highest confidence identification.

        @return:
        """
        tracker = Tracker()

        box_collection = BoundingBoxCollection()
        box_collection.add(Box(0.1, 0.4, 0.1, 0.6, 0.5, "test1"))
        tracker.add_new_frame(copy.deepcopy(box_collection))

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(Box(0.1, 0.4, 0.1, 0.6, 0.7, "test2"))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        expected_result = box_collection_2
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks after higher confidence classification: \n" + str(expected_result) +
                              "\n does not equal tracked items: \n" + str(actual_result)))

    def test_returns_most_likely_object_classification_after_lower_likelihood_classification(self):
        """
        Tests that the tracker still returns the most likely item classification , even after it stops being the most
        recent.

        @return:
        """
        tracker = Tracker()

        box_collection = BoundingBoxCollection()
        box_collection.add(Box(0.1, 0.4, 0.1, 0.6, 0.5, "possibly this"))
        tracker.add_new_frame(copy.deepcopy(box_collection))

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(Box(0.1, 0.4, 0.1, 0.6, 0.7, "probably this"))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        tracker.add_new_frame(copy.deepcopy(box_collection))

        expected_result = box_collection_2
        actual_result, _ = tracker.get_current_tracks()
        self.assertEqual(expected_result, actual_result,
                         msg=("Expected tracks after higher confidence classification: \n" + str(expected_result) +
                              "\n does not equal tracked items: \n" + str(actual_result)))

    def test_tracker_returns_empty_list_of_track_ids_when_no_tracks(self):
        """
        Test that the tracker returns an empty list of track unique id numbers when there are no tracks.

        @return:
        """
        tracker = Tracker()

        box_collection = BoundingBoxCollection()
        tracker.add_new_frame(copy.deepcopy(box_collection))

        expected_result = list()
        _, actual_result = tracker.get_current_tracks()

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected track ids: \n" + str(expected_result) +
                              "\n does not equal actual track ids: \n" + str(actual_result)))

    def test_tracker_returns_unique_track_ids(self):
        """
        Test that the tracker returns a list of the unique ids for each current track.

        @return:
        """
        tracker = Tracker()

        box_collection = BoundingBoxCollection()
        box_0 = Box(0.2, 0.3, 0.2, 0.6, 0.5, "test1")
        box_1 = Box(0.1, 0.4, 0.1, 0.6, 0.5, "test2")
        box_2 = Box(0.0, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection.add(box_0)
        box_collection.add(box_1)
        box_collection.add(box_2)

        tracker.add_new_frame(copy.deepcopy(box_collection))

        expected_result = [0, 1, 2]
        _, actual_result = tracker.get_current_tracks()

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected track ids: \n" + str(expected_result) +
                              "\n does not equal actual track ids: \n" + str(actual_result)))

    def test_tracker_returns_correct_uid_list_after_item_no_longer_tracked(self):
        """
        Test tracker returns the correct list of unique id numbers after an item stops being tracked.

        @return:
        """
        tracker = Tracker(allowed_absence=1)

        box_0 = Box(0.0, 0.1, 0.0, 0.1, 0.5, "test1")
        box_1 = Box(0.1, 0.2, 0.1, 0.2, 0.5, "test2")
        box_2 = Box(0.2, 0.3, 0.2, 0.3, 0.7, "test3")

        box_collection_1 = BoundingBoxCollection()
        box_collection_1.add(box_0)
        box_collection_1.add(box_1)
        box_collection_1.add(box_2)

        box_collection_2 = BoundingBoxCollection()
        box_collection_2.add(box_0)
        box_collection_2.add(box_2)

        tracker.add_new_frame(copy.deepcopy(box_collection_1))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))
        tracker.add_new_frame(copy.deepcopy(box_collection_2))

        expected_result = [0, 2]
        _, actual_result = tracker.get_current_tracks()

        self.assertEqual(expected_result, actual_result,
                         msg=("Expected track ids: \n" + str(expected_result) +
                              "\n does not equal actual track ids: \n" + str(actual_result)))
