from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box
from util.Debugging import debug_print


class Tracker:

    def __init__(self):
        self.__tracks__: BoundingBoxCollection = BoundingBoxCollection()
        self.__age_of_tracks__: list = list()
        self.__frame_count__: int = 0
        self.__allowed_absence__ = 0

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

        for i in sorted(indexes_to_remove, reverse=True):
            self.__age_of_tracks__.pop(i)
            self.__tracks__.pop(i)

    def __add_frame_bounding_boxes_to_tracks__(self, frame_boxes: BoundingBoxCollection):
        track_age = self.__frame_count__

        for i in range(frame_boxes.size()):
            box = frame_boxes.get(i)
            if not self.__tracks__.contains(box):
                self.__tracks__.add(box)
                self.__age_of_tracks__.append(track_age)
            else:
                self.__age_of_tracks__[i] = track_age

    def get_current_tracks(self) -> BoundingBoxCollection:
        return self.__tracks__

    def set_allowed_absence(self, allowed_absence: int):
        self.__allowed_absence__ = allowed_absence
