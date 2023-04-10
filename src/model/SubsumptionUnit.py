from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box
from util.Debugging import debug_print


class SubsumptionUnit:
    def __init__(self):
        self.iou_threshold: float = 0.9
        self.__subsumption_lists__: list = list()
        self.__items_to_sub_into__: list = list()
        self.__items_that_can_be_subbed__: list = list()
        self.__items_to_sub__: dict = dict()

    def add_list(self, new_list: list):
        item = new_list.pop(0)
        self.__subsumption_lists__.append(new_list)
        self.__items_to_sub_into__.append(item)
        self.__add_new_items_that_can_be_subbed__(new_list)

        can_be_substituted_for = item
        for sub_able_item in new_list:
            if not self.__items_to_sub__.__contains__(sub_able_item):
                self.__items_to_sub__[sub_able_item] = [can_be_substituted_for]
            else:
                self.__items_to_sub__[sub_able_item].append(can_be_substituted_for)

    def __add_new_items_that_can_be_subbed__(self, new_list: list):
        for item in new_list:
            if not self.__items_that_can_be_subbed__.__contains__(item):
                self.__items_that_can_be_subbed__.append(item)

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

        debug_print("box to sub: ", box)
        debug_print("list of items can sub into:", list_of_items_can_sub_into)
        debug_print("IoU threshold: ", self.iou_threshold)

        for candidate_box in boxes:
            debug_print("candidate: ", candidate_box)
            if candidate_box.label in list_of_items_can_sub_into:
                iou = candidate_box.get_iou(box)
                debug_print("iou: ", iou)
                if iou > self.iou_threshold:
                    debug_print()
                    return True

        return False
