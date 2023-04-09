from util.BoundingBoxCollection import BoundingBoxCollection
from util.SafeListEditor import safely_remove_list_indexes as safe_del


class KnowledgeUnit:

    def __init__(self):
        self.__seen_items__: list = list()
        self.__item_counts__: list = list()
        self.__time_item_last_seen__: list = list()

    def get_seen_items(self) -> list:
        return sorted(self.__seen_items__)

    def add_frame(self, frame_boxes: BoundingBoxCollection, time: int):

        frame: KnowledgeUnit.Frame = KnowledgeUnit.Frame(frame_boxes)

        for i in range(len(frame.item_types)):
            item = frame.item_types[i]
            count = frame.item_counts[i]
            if not self.__seen_items__.__contains__(item):
                self.__seen_items__.append(item)
                self.__item_counts__.append(count)
                self.__time_item_last_seen__.append(time)
            else:
                index = self.__seen_items__.index(item)
                if self.__item_counts__[index] < count:
                    self.__item_counts__[index] = count
                    self.__time_item_last_seen__[index] = time

    def how_many_have_you_seen(self, item_label: str) -> int:
        for i in range(len(self.__seen_items__)):
            if self.__seen_items__[i] == item_label:
                return self.__item_counts__[i]
        return 0

    class Frame:
        def __init__(self, bboxes: BoundingBoxCollection):
            self.bboxes: BoundingBoxCollection = bboxes
            self.item_types: list = list()
            self.item_counts: list = list()

            for box in bboxes:
                label = box.label
                if not self.item_types.__contains__(label):
                    self.item_types.append(label)
                    self.item_counts.append(1)
                else:
                    index = self.item_types.index(label)
                    self.item_counts[index] += 1

    def how_long_since_you_saw(self, item: str, current_time: int):
        if self.__seen_items__.__contains__(item):
            index = self.__seen_items__.index(item)
            return self.__time_item_last_seen__[index]
        else:
            return -1

