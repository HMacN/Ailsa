import copy

from util.BoundingBoxCollection import BoundingBoxCollection
from util.SafeListEditor import safely_remove_list_indexes as safe_rm
from util.Box import Box
from util.Debugging import debug_print


class Tracker:

    def __init__(self, iou_threshold=0.9, min_frames=1, allowed_absence=0):
        self.__tracks_2__: list = list()
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
        for i in range(len(self.__tracks_2__)):
            track: Tracker.Track = self.__tracks_2__[i]
            if track.get_last_seen() < oldest_allowed_track:
                indexes_to_remove.append(i)

        safe_rm(self.__tracks_2__, indexes_to_remove)

    def __add_frame_bounding_boxes_to_tracks__(self, frame_boxes: BoundingBoxCollection):
        bbox_indexes_to_remove = list()

        for track_index in range(len(self.__tracks_2__)):
            for bbox_index in range(frame_boxes.size()):
                if self.__update_track_if_box_overlaps__(track_index, bbox_index, frame_boxes):
                    bbox_indexes_to_remove.append(bbox_index)
            self.__get_rid_of_boxes_that_are_now_updated_tracks__(frame_boxes, bbox_indexes_to_remove)
        self.__add_remaining_boxes_as_new_tracks__(frame_boxes)

    def __update_track_if_box_overlaps__(self, track_index: int, box_index: int, boxes: BoundingBoxCollection) -> bool:
        existing_track: Tracker.Track = self.__tracks_2__[track_index]
        new_bbox: Box = boxes[box_index]
        current_frame = copy.deepcopy(self.__frame_count__)
        iou_threshold = self.__min_iou_to_continue_track__

        iou = existing_track.get_box().get_iou(new_bbox)
        if iou > iou_threshold:
            existing_track.sighted(new_bbox, current_frame)
            return True
        else:
            return False

    @classmethod
    def __get_rid_of_boxes_that_are_now_updated_tracks__(cls, boxes, indexes: list):
        safe_rm(boxes, indexes)

    def __add_remaining_boxes_as_new_tracks__(self, frame_boxes: BoundingBoxCollection):
        current_frame = copy.deepcopy(self.__frame_count__)
        for remaining_bbox in frame_boxes:
            new_track = Tracker.Track(remaining_bbox, current_frame)
            self.__tracks_2__.append(new_track)

    def get_current_tracks(self) -> BoundingBoxCollection:
        active_tracks = BoundingBoxCollection()
        for index in range(len(self.__tracks_2__)):
            track: Tracker.Track = self.__tracks_2__[index]
            if track.get_frames_detected() >= self.__min_frames_for_track__:
                active_tracks.add(track.get_box())
        return copy.deepcopy(active_tracks)

    class Track:

        def __init__(self, box: Box, frame_last_seen: int):
            self.__box__: Box = box
            self.__last_seen__: int = frame_last_seen
            self.__detected_for__: int = 1

        def lost_contact(self):
            self.__detected_for__ = 0

        def sighted(self, box: Box, frame: int):
            self.__box__ = box
            self.__last_seen__ = frame
            self.__detected_for__ += 1

        def get_last_seen(self) -> int:
            return self.__last_seen__

        def get_box(self) -> Box:
            return self.__box__

        def get_frames_detected(self) -> int:
            return self.__detected_for__

