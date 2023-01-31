from util.DebugPrint import debug_print
from util.IdentifiedObject import IdentifiedObject


class DetectedObjectRegister:

    def __init__(self):
        self.__list_of_items = list()

    def add(self, item: IdentifiedObject):

        if item not in self.__list_of_items:
            self.__list_of_items.append(item)

    def get_by_name(self, name: str) -> list:
        def selection_function(item: IdentifiedObject) -> bool:
            return item.get_object_name() == name

        return self.__get_sublist(selection_function)

    def get_between_horiz_origin_and(self, horiz_coord: int) -> list:
        def selection_function(item: IdentifiedObject) -> bool:
            return (item.horizontal_distance_to_origin + item.bounding_box_width) <= horiz_coord

        return self.__get_sublist(selection_function)

    def get_between_horiz_far_edge_and(self, horiz_coord: int) -> list:
        def selection_function(item: IdentifiedObject) -> bool:
            return item.horizontal_distance_to_origin >= horiz_coord

        return self.__get_sublist(selection_function)

    def get_between_vert_origin_and(self, vert_coord: int) -> list:
        def selection_function(item: IdentifiedObject) -> bool:
            return (item.vertical_distance_to_origin + item.bounding_box_height) <= vert_coord

        return self.__get_sublist(selection_function)

    def get_between_vert_far_edge_and(self, vert_coord: int) -> list:
        def selection_function(item: IdentifiedObject) -> bool:
            return item.vertical_distance_to_origin >= vert_coord

        return self.__get_sublist(selection_function)

    def get_all(self):
        return self.__list_of_items

    def get_horiz_overlapping_for(self, item: IdentifiedObject):
        def selection_function(other: IdentifiedObject) -> bool:

            debug_print(item, other)
            if item is other:
                return False

            item_right_edge = item.horizontal_distance_to_origin + item.bounding_box_width
            item_left_edge = item.horizontal_distance_to_origin
            other_right_edge = other.horizontal_distance_to_origin + other.bounding_box_width
            other_left_edge = other.horizontal_distance_to_origin

            if item_right_edge < other_left_edge:
                return False

            if item_left_edge > other_right_edge:
                return False

            return True

        return self.__get_sublist(selection_function)

    def get_vert_overlapping_for(self, item: IdentifiedObject):
        def selection_function(other: IdentifiedObject) -> bool:

            debug_print(item, other)
            if item is other:
                return False

            item_top_edge = item.vertical_distance_to_origin + item.bounding_box_height
            item_bottom_edge = item.vertical_distance_to_origin
            other_top_edge = other.vertical_distance_to_origin + other.bounding_box_height
            other_bottom_edge = other.vertical_distance_to_origin

            if item_top_edge < other_bottom_edge:
                return False

            if item_bottom_edge > other_top_edge:
                return False

            return True

        return self.__get_sublist(selection_function)

    def __get_sublist(self, selection_function) -> list:
        list_to_return = list()

        for i in range(len(self.__list_of_items)):
            item: IdentifiedObject = self.__list_of_items[i]

            if selection_function(self.__list_of_items[i]):
                list_to_return.append(item)

        return list_to_return



