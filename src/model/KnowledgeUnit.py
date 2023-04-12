from util.BoundingBoxCollection import BoundingBoxCollection
from util.Debugging import debug_print
from util.SafeListEditor import safely_remove_list_indexes as safe_del


class KnowledgeUnit:

    def __init__(self):
        self.__impossible_items__: list = list()
        self.__seen_items__: list = list()
        self.__item_counts__: list = list()
        self.__time_item_last_seen__: list = list()
        self.__facts__: KnowledgeUnit.Facts = KnowledgeUnit.Facts()
        self.__last_frame__: KnowledgeUnit.Frame | None = None

    def get_list_of_all_seen_items(self) -> list:
        return sorted(self.__seen_items__)

    def add_frame(self, frame_boxes: BoundingBoxCollection, time: int):

        frame: KnowledgeUnit.Frame = KnowledgeUnit.Frame(frame_boxes)
        self.__rename_impossible_items_in_frame__(frame)
        self.__last_frame__ = frame

        for i in range(len(frame.item_types)):
            item = frame.item_types[i]
            count = frame.item_counts[i]
            impossible = item in self.__impossible_items__
            if not self.__seen_items__.__contains__(item):
                self.__add_new_item__(item, count, time)
            elif not impossible:
                index = self.__seen_items__.index(item)
                self.__update_item_counts__(count, index)
                self.__update_list_of_times_item_seen__(index, time)

    def __rename_impossible_items_in_frame__(self, frame: 'KnowledgeUnit.Frame'):
        for i in range(len(frame.item_types)):
            if frame.item_types[i] in self.__impossible_items__:
                frame.item_types[i] = "unknown item"

    def __update_list_of_times_item_seen__(self, index: int, time: int):
        list_of_times_item_seen: list = self.__time_item_last_seen__[index]
        if list_of_times_item_seen[-1] == time - 1:
            list_of_times_item_seen[-1] = time
        else:
            list_of_times_item_seen.append(time)

    def __update_item_counts__(self, count: int, index: int):
        if self.__item_counts__[index] < count:
            self.__item_counts__[index] = count

    def __add_new_item__(self, item: str, count: int, time: int):
        self.__seen_items__.append(item)
        self.__item_counts__.append(count)
        self.__time_item_last_seen__.append([time])

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

    def when_did_you_see(self, item: str):
        if self.__seen_items__.__contains__(item):
            index = self.__seen_items__.index(item)
            return self.__time_item_last_seen__[index]
        else:
            return list()

    def where_did_you_see(self, item: str) -> list:
        if self.__seen_items__.__contains__(item):
            if self.__facts__.items_not_normally_on_floor.__contains__(item):
                return ["on the floor"]
            return [""]
        return list()

    def set_items_not_normally_on_floor(self, items: list):
        self.__facts__.items_not_normally_on_floor = items

    class Facts:
        def __init__(self):
            self.items_not_normally_on_floor: list = list()

    def set_impossible_items(self, items: list):
        self.__impossible_items__ = items

    def describe_scene(self) -> dict:
        description = dict()
        items: list = self.__last_frame__.item_types

        description["ahead of you"] = items

        return description
