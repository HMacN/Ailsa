from util.DebugPrint import debug_print
from util.IdentifiedObject import IdentifiedObject


def are_boxes_overlapping_on_one_axis(item_far_edge: int, item_near_edge: int, other_far_edge: int,
                                      other_near_edge: int) -> bool:
    if item_far_edge < other_near_edge:
        return False

    if item_near_edge > other_far_edge:
        return False

    return True


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
            if item is other:
                return False

            return are_boxes_overlapping_on_one_axis(item.horizontal_distance_to_origin + item.bounding_box_width,
                                                     item.horizontal_distance_to_origin,
                                                     other.horizontal_distance_to_origin + other.bounding_box_width,
                                                     other.horizontal_distance_to_origin)

        return self.__get_sublist(selection_function)

    def get_vert_overlapping_for(self, item: IdentifiedObject):
        def selection_function(other: IdentifiedObject) -> bool:
            if item is other:
                return False

            return are_boxes_overlapping_on_one_axis(item.vertical_distance_to_origin + item.bounding_box_height,
                                                     item.vertical_distance_to_origin,
                                                     other.vertical_distance_to_origin + other.bounding_box_height,
                                                     other.vertical_distance_to_origin)

        return self.__get_sublist(selection_function)

    def __get_sublist(self, selection_function) -> list:
        list_to_return = list()

        for i in range(len(self.__list_of_items)):
            item: IdentifiedObject = self.__list_of_items[i]

            if selection_function(self.__list_of_items[i]):
                list_to_return.append(item)

        return list_to_return
