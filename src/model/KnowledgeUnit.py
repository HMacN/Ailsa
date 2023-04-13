from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box


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

        frame_boxes.sort_by_area()
        frame: KnowledgeUnit.Frame = KnowledgeUnit.Frame(frame_boxes)
        self.__rename_impossible_items_in_frame__(frame)
        self.__last_frame__ = frame

        for i in range(len(frame.item_types)):
            item_name = frame.item_types[i]
            count = frame.item_counts[i]
            impossible = item_name in self.__impossible_items__
            if not self.__seen_items__.__contains__(item_name):
                self.__add_new_item__(item_name, count, time)
            elif not impossible:
                index = self.__seen_items__.index(item_name)
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
            self.wall_and_ceiling_items: list = list()
            self.furniture_items: list = list()
            self.left_frame_boundary = 0.33
            self.right_frame_boundary = 0.66
            self.custom_categories: dict = dict()
            self.max_gap_for_item_on_top_of_another: float = 0.0

    def set_impossible_items(self, items: list):
        self.__impossible_items__ = items

    def describe_scene(self) -> dict:
        description = dict()
        items: BoundingBoxCollection = self.__last_frame__.bboxes
        items_ahead: list = list()
        items_left: list = list()
        items_right: list = list()

        for item in items:
            if self.__item_is_ahead__(item):
                items_ahead.append(item.label)
            if self.__item_is_left__(item):
                items_left.append(item.label)
            if self.__item_is_right__(item):
                items_right.append(item.label)

        description["ahead"] = sorted(items_ahead)
        description["left"] = sorted(items_left)
        description["right"] = sorted(items_right)

        for custom_category in self.__facts__.custom_categories.keys():
            category_items: list = list()
            for item in items:
                if item.label in self.__facts__.custom_categories[custom_category]:
                    category_items.append(item.label)
            description[custom_category] = sorted(category_items)

        return description

    def __item_is_right__(self, item: Box) -> bool:
        return item.right_edge > self.__facts__.right_frame_boundary

    def __item_is_left__(self, item: Box) -> bool:
        return item.left_edge < self.__facts__.left_frame_boundary

    def __item_is_ahead__(self, item: Box) -> bool:
        return item.right_edge > self.__facts__.left_frame_boundary \
                and item.left_edge < self.__facts__.right_frame_boundary

    def set_left_and_right(self, left_boundary: float, right_boundary: float):
        self.__facts__.left_frame_boundary = left_boundary
        self.__facts__.right_frame_boundary = right_boundary

    def set_custom_category(self, name: str, items: list):
        self.__facts__.custom_categories[name] = items

    def get_list_of_seen_items_in_category(self, category: str) -> list:
        seen_category_items: list = list()
        for item_name in self.__seen_items__:
            if item_name in self.__facts__.custom_categories[category]:
                seen_category_items.append(item_name)
        return seen_category_items

    def where_is(self, item_name: str) -> dict:
        item_location: dict = dict()
        frame_bboxes: BoundingBoxCollection = self.__last_frame__.bboxes

        for item in frame_bboxes:
            if item.label == item_name:
                item_location["direction"] = self.__get_direction_list__(item)
                item_location["beneath"] = self.__get_beneath_list__(item)
                item_location["on top of"] = self.__get_on_top_of__(item)
                return item_location

        return item_location

    def __get_on_top_of__(self, item_on_top: Box) -> str:
        object_item_is_on_top_of = ""
        if item_on_top.label in self.__facts__.furniture_items:
            return object_item_is_on_top_of

        max_area_below: float = 0.0
        frame_items: BoundingBoxCollection = self.__last_frame__.bboxes
        for item_below in frame_items:
            high_enough_to_sit_on = item_below.upper_edge + self.__facts__.max_gap_for_item_on_top_of_another
            if high_enough_to_sit_on > item_on_top.lower_edge:
                if item_below.left_edge < item_on_top.right_edge and item_below.right_edge > item_on_top.left_edge:
                    if item_below is not item_on_top:
                        area_below = item_below.get_overlap_area(Box(0.0, 1.0, 0.0, item_on_top.lower_edge, 1.0, ""))
                        if area_below > max_area_below:
                            max_area_below = area_below
                            object_item_is_on_top_of = item_below.label

        return object_item_is_on_top_of

    def __get_beneath_list__(self, item_beneath: Box) -> list:
        item_beneath_these_objects: list = list()

        frame_items: BoundingBoxCollection = self.__last_frame__.bboxes
        for item_above in frame_items:
            if item_above.label in self.__facts__.wall_and_ceiling_items:
                if item_above.lower_edge > item_beneath.lower_edge:
                    if item_above.right_edge > item_beneath.left_edge \
                            and item_above.left_edge < item_beneath.right_edge:
                        item_beneath_these_objects.append(item_above.label)

        return sorted(item_beneath_these_objects)

    def __get_direction_list__(self, item: Box) -> list:
        direction: list = list()
        if self.__item_is_ahead__(item):
            direction.append("ahead")
        if self.__item_is_left__(item):
            direction.append("left")
        if self.__item_is_right__(item):
            direction.append("right")
        return sorted(direction)

    def add_wall_and_ceiling_objects(self, objects: list):
        self.__facts__.wall_and_ceiling_items = objects

    def set_furniture_items(self, furniture_items: list):
        self.__facts__.furniture_items = furniture_items

    def items_between_user_and(self, item_name: str) -> list:
        for item in self.__last_frame__.bboxes:
            if item.label == item_name:
                return self.__get_intervening_items__(item)

        return list()

    def __get_intervening_items__(self, target_item: Box) -> list:
        intervening_items: list = list()

        for intervening_item in self.__last_frame__.bboxes:
            if intervening_item.lower_edge < target_item.lower_edge \
                    and intervening_item is not target_item:
                intervening_items.append(intervening_item.label)

        return intervening_items

    def set_max_gap_for_item_on_top_of_another_item(self, max_gap: float):
        self.__facts__.max_gap_for_item_on_top_of_another = max_gap


