from util.BoundingBoxCollection import BoundingBoxCollection


class Tracker:

    def __init__(self):
        self.__tracks__: BoundingBoxCollection | None = None

    def add_new_frame(self, bounding_boxes: BoundingBoxCollection):
        self.__tracks__ = bounding_boxes

    def get_current_tracks(self) -> BoundingBoxCollection | None:
        return self.__tracks__
