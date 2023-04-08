import copy

from util.BoundingBoxCollection import BoundingBoxCollection
from util.SafeListEditor import safely_remove_list_indexes as safe_rm
from util.Box import Box
from util.Debugging import debug_print


class Tracker:

    def __init__(self, iou_threshold=0.9, min_frames=1, allowed_absence=0):
        self.__tracks__: BoundingBoxCollection = BoundingBoxCollection()
        self.__tracks_2__: list = list()
        self.__track_last_detected_on_frame__: list = list()
        self.__track_detected_for_frames__: list = list()
        self.__frame_count__: int = 0
        self.__min_frames_for_track__ = min_frames
        self.__allowed_absence__ = allowed_absence
        self.__min_iou_to_continue_track__ = iou_threshold

    def add_new_frame(self, frame_bounding_boxes: BoundingBoxCollection):
        self.__frame_count__ = self.__frame_count__ + 1
        self.__add_frame_bounding_boxes_to_tracks__(frame_bounding_boxes)
        self.__remove_old_tracks__()

    def __remove_old_tracks__(self):
        oldest_allowed_track = self.__frame_count__ - self.__allowed_absence__
        indexes_to_remove = list()
        for i in range(self.__tracks__.size()):
            if self.__track_last_detected_on_frame__[i] < oldest_allowed_track:
                indexes_to_remove.append(i)

        safe_rm(self.__track_last_detected_on_frame__, indexes_to_remove)
        safe_rm(self.__tracks__, indexes_to_remove)
        safe_rm(self.__track_detected_for_frames__, indexes_to_remove)

    def __add_frame_bounding_boxes_to_tracks__(self, frame_boxes: BoundingBoxCollection):
        new_track_age = self.__frame_count__
        bbox_indexes_to_remove = list()

        for track_index in range(self.__tracks__.size()):
            for bbox_index in range(frame_boxes.size()):
                if self.__update_track_if_box_overlaps__(track_index, bbox_index, frame_boxes):
                    bbox_indexes_to_remove.append(bbox_index)
            self.__get_rid_of_boxes_that_are_now_updated_tracks__(frame_boxes, bbox_indexes_to_remove)
        self.__add_remaining_boxes_as_new_tracks__(frame_boxes, new_track_age)

    def __update_track_if_box_overlaps__(self, track_index: int, box_index: int, boxes: BoundingBoxCollection) -> bool:
        existing_track: Box = self.__tracks__[track_index]
        new_bbox: Box = copy.deepcopy(boxes[box_index])
        current_frame = copy.deepcopy(self.__frame_count__)
        iou_threshold = self.__min_iou_to_continue_track__

        track = Tracker.Track(new_bbox, current_frame)

        iou = existing_track.get_iou(new_bbox)
        if iou > iou_threshold:
            self.__tracks_2__.append(track)
            self.__tracks__[track_index] = new_bbox
            self.__track_last_detected_on_frame__[track_index] = current_frame
            self.__track_detected_for_frames__[track_index] += 1
            return True
        else:
            return False

    @classmethod
    def __get_rid_of_boxes_that_are_now_updated_tracks__(cls, boxes, indexes: list):
        safe_rm(boxes, indexes)

    def __add_remaining_boxes_as_new_tracks__(self, frame_boxes: BoundingBoxCollection, new_track_age: int):
        for remaining_bbox in frame_boxes:
            self.__tracks__.add(remaining_bbox)
            self.__track_last_detected_on_frame__.append(new_track_age)
            self.__track_detected_for_frames__.append(1)

    def get_current_tracks(self) -> BoundingBoxCollection:
        active_tracks = BoundingBoxCollection()

        for index in range(len(self.__tracks__)):
            if self.__track_detected_for_frames__[index] >= self.__min_frames_for_track__:
                active_tracks.add(self.__tracks__[index])

        return copy.deepcopy(active_tracks)

    class Track:

        def __init__(self, box: Box, frame_last_seen: int):
            self.box: Box = box
            self.last_seen: int = frame_last_seen
            self.detected_for: int = 1

        def lost_contact(self):
            self.detected_for = 0

        def seen_on_frame(self, frame: int):
            self.last_seen = frame
            self.detected_for += 1
