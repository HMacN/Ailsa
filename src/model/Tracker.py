from util.BoundingBoxCollection import BoundingBoxCollection


class Tracker:

    def __init__(self):
        self.__tracks__: BoundingBoxCollection = BoundingBoxCollection()

    def add_new_frame(self, bounding_boxes: BoundingBoxCollection):
        for i in range(bounding_boxes.size()):
            box = bounding_boxes.get(i)
            if not self.__tracks__.contains(box):
                self.__tracks__.add(box)

    def get_current_tracks(self) -> BoundingBoxCollection | None:
        return self.__tracks__
