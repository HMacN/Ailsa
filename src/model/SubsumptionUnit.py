from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box


class SubsumptionUnit:
    def __init__(self):
        self.__overlap_threshold__: float = 0.9
        self.__items_to_sub__: dict = dict()

    def add_list(self, new_list: list):
        item = new_list.pop(0)

        can_be_substituted_for = item
        for sub_able_item in new_list:
            if sub_able_item not in self.__items_to_sub__:
                self.__items_to_sub__[sub_able_item] = [can_be_substituted_for]
            else:
                self.__items_to_sub__[sub_able_item].append(can_be_substituted_for)

    def subsume_bboxes(self, boxes: BoundingBoxCollection) -> BoundingBoxCollection:
        boxes_to_return: BoundingBoxCollection = BoundingBoxCollection()
        boxes.sort_by_area()
        list_of_boxes_subbed_into_own_type: list = [False] * len(boxes)
        for index in range(len(boxes)):
            box_subbed, subbed_into_own_type = self.__try_to_sub_box__(index, boxes, list_of_boxes_subbed_into_own_type)
            if not box_subbed:
                boxes_to_return.add(boxes[index])
            if subbed_into_own_type:
                list_of_boxes_subbed_into_own_type[index] = True

        return boxes_to_return

    def __try_to_sub_box__(self, index_of_box_to_be_subbed: int,
                           boxes: BoundingBoxCollection,
                           list_of_boxes_subbed_into_own_type: list) -> (bool, bool):
        box_to_be_subbed = boxes[index_of_box_to_be_subbed]
        list_of_items_can_sub_into: list = self.__generate_list_of_possible_boxes_to_sub_into__(box_to_be_subbed)

        for i in range(len(boxes)):
            candidate_box = boxes[i]

            candidate_can_be_subbed_into = candidate_box.label in list_of_items_can_sub_into
            they_are_not_the_same_box = candidate_box != box_to_be_subbed
            candidate_was_not_subbed_into_own_type = not list_of_boxes_subbed_into_own_type[i]
            if candidate_can_be_subbed_into \
                    and they_are_not_the_same_box \
                    and candidate_was_not_subbed_into_own_type:
                if self.__check_if_overlapping__(box_to_be_subbed, candidate_box):
                    subbed_into_own_type = box_to_be_subbed.label == candidate_box.label
                    return True, subbed_into_own_type
        return False, False

    def __check_if_overlapping__(self, overlapping_box: Box, overlapped_box: Box) -> bool:
        overlap_area = overlapped_box.get_overlap_area(overlapping_box)
        overlap_ratio = overlap_area / overlapping_box.get_area()
        return overlap_ratio > self.__overlap_threshold__

    def __generate_list_of_possible_boxes_to_sub_into__(self, box_to_be_subbed: Box) -> list:
        list_of_items_can_sub_into: list = [box_to_be_subbed.label]
        if box_to_be_subbed.label in self.__items_to_sub__:
            list_of_items_can_sub_into.extend(self.__items_to_sub__[box_to_be_subbed.label])
        return list_of_items_can_sub_into

    def set_overlap_threshold(self, allowed_overlap=0.9):
        self.__overlap_threshold__ = allowed_overlap
