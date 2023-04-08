from util.BoundingBoxCollection import BoundingBoxCollection


class KnowledgeUnit:

    def __init__(self):
        self.__seen_items__: list = list()

    def get_seen_items(self) -> list:
        return sorted(self.__seen_items__)

    def add_frame(self, frame: BoundingBoxCollection):
        for box in frame:
            label = box.label
            if not self.__seen_items__.__contains__(label):
                self.__seen_items__.append(label)
