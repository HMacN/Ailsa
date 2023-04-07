import copy

from util.BoundingBoxCollection import BoundingBoxCollection
from util.SafeListEditor import safely_remove_list_indexes as safe_rm
from util.Box import Box
from util.Debugging import debug_print


class Tracker:

    def __init__(self):
        self.__tracks__: BoundingBoxCollection = BoundingBoxCollection()
        self.__age_of_tracks__: list = list()
        self.__frame_count__: int = 0
        self.__allowed_absence__ = 0
        self.__min_iou_to_continue_track__ = 0.9

    def add_new_frame(self, frame_bounding_boxes: BoundingBoxCollection):
        self.__frame_count__ = self.__frame_count__ + 1
        self.__add_frame_bounding_boxes_to_tracks__(frame_bounding_boxes)
        self.__remove_old_tracks__()

    def __remove_old_tracks__(self):
        oldest_allowed_track = self.__frame_count__ - self.__allowed_absence__
        indexes_to_remove = list()
        for i in range(self.__tracks__.size()):
            if self.__age_of_tracks__[i] < oldest_allowed_track:
                indexes_to_remove.append(i)

        safe_rm(self.__age_of_tracks__, indexes_to_remove)
        safe_rm(self.__tracks__, indexes_to_remove)

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
        new_bbox: Box = boxes[box_index]
        iou_threshold = self.__min_iou_to_continue_track__

        if existing_track.get_iou(new_bbox) > iou_threshold:
            self.__tracks__[track_index] = copy.deepcopy(new_bbox)
            self.__age_of_tracks__[track_index] = self.__frame_count__
            return True
        else:
            return False

    @classmethod
    def __get_rid_of_boxes_that_are_now_updated_tracks__(cls, boxes, indexes: list):
        safe_rm(boxes, indexes)

    def __add_remaining_boxes_as_new_tracks__(self, frame_boxes: BoundingBoxCollection, new_track_age: int):
        for remaining_bbox in frame_boxes:
            self.__tracks__.add(remaining_bbox)
            self.__age_of_tracks__.append(new_track_age)

    def get_current_tracks(self) -> BoundingBoxCollection:
        return self.__tracks__

    def set_allowed_absence(self, allowed_absence: int):
        self.__allowed_absence__ = allowed_absence
