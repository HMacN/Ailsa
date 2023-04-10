from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box
from util.Debugging import debug_print


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
        for index in range(len(boxes)):
            if boxes[index].label in self.__items_to_sub__:
                box_subbed = self.__try_to_sub_box__(index, boxes)
                if not box_subbed:
                    boxes_to_return.add(boxes[index])
            else:
                boxes_to_return.add(boxes[index])

        return boxes_to_return

    def __try_to_sub_box__(self, box_index: int, boxes: BoundingBoxCollection) -> bool:
        box = boxes[box_index]
        list_of_items_can_sub_into = self.__items_to_sub__[box.label]

        for candidate_box in boxes:
            if candidate_box.label in list_of_items_can_sub_into:
                overlap = candidate_box.get_overlap_area(box)
                if overlap / box.get_area() > self.__overlap_threshold__:
                    return True

        return False
