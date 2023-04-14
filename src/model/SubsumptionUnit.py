from util.BoxList import BoxList
from util.Box import Box


class SubsumptionUnit:
    """
    A class to perform an alternative to Non-Maximum Suppression (NMS).  Takes lists of items which can be subsumed by
    each other, and then will remove (subsume) bounding boxes which overlap with each other if they are on the same
    subsumption list.  This is to avoid the problem with NMS where, for example, items on top of a table are suppressed
    and not reported to the user.  It should also help stop the problem of multiple overlapping bounding boxes all being
    reported for the same item.
    """
    def __init__(self):
        """The constructor.  Defines the default value for the overlap threshold."""
        self.__overlap_threshold__: float = 0.9
        self.__items_to_sub__: dict = dict()

    def add_list(self, new_list: list):
        """
        Adds a list of items that can be subsumed into the bounding box of a given item.  The first item category in the
        list (at element 0) is the item category that the other items in the list will be subsumed into, if they have a
        suitably large overlap with an appropriate bounding box.

        @param new_list:    A list of str values describing the item type to subsume into, and the item types that may
                            be subsumed.
        @return:
        """
        item = new_list.pop(0)

        can_be_substituted_for = item
        for sub_able_item in new_list:
            if sub_able_item not in self.__items_to_sub__:
                self.__items_to_sub__[sub_able_item] = [can_be_substituted_for]
            else:
                self.__items_to_sub__[sub_able_item].append(can_be_substituted_for)

    def subsume_bboxes(self, boxes: BoxList) -> BoxList:
        """
        Perform subsumption on the given list of bounding boxes.  Bounding boxes of the same type, and of types which
        may be subsumed into the appropriate type, are removed if they have a suitably large overlap with another
        bounding box.

        @param boxes:   A BoxList object which contains the list of bounding boxes to subsume into each
                        other if possible.
        @return:        A BoxList object that has had boxes that can be subsumed into another box removed.
        """
        boxes_to_return: BoxList = BoxList()
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
                           boxes: BoxList,
                           list_of_boxes_subbed_into_own_type: list) -> (bool, bool):
        """
        Attempts to subsume a given bounding box into another, and returns a boolean describing if this could be done.
        Also returns a bool describing if the bounding box was subsumed into a box of its own type, which is needed to
        stop boxes of the same type "pairing up" and subsuming into each other.

        @param index_of_box_to_be_subbed:           An int which is the index of the target box in the box collection.
        @param boxes:                               A BoxList object containing the boxes to try to
                                                    subsume the target box into.
        @param list_of_boxes_subbed_into_own_type:  A list of bool values describing which indexes in the box collection
                                                    have been subsumed into boxes of their own type.
        @return:                                    A tuple of two bool values.  The first describes whether or not the
                                                    given bounding box could be subsumed into another one, and the
                                                    second describes whether or not it was subsumed into a bounding box
                                                    of its own type.
        """
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
        """
        Checks if two boxes have a suitably large overlap.  This is defined as whether or not the overlapping area (as a
        decimal of the area of the given box) is larger than the overlap threshold value.

        @param overlapping_box: A Box object, which may or may not overlap with another box.
        @param overlapped_box:  A Box object, which may or may not overlap with the given box.
        @return:                A bool, which describes if the given boxes overlap by more than the threshold.
        """
        overlap_area = overlapped_box.get_overlap_area(overlapping_box)
        overlap_ratio = overlap_area / overlapping_box.get_area()
        return overlap_ratio > self.__overlap_threshold__

    def __generate_list_of_possible_boxes_to_sub_into__(self, box_to_be_subbed: Box) -> list:
        """
        Checks the lists of valid subsumption options and returns a list of all possible item labels that the given
        bounding box may be subsumed into.  This list automatically includes the name of the item type of the given
        bounding box.  I.e. bounding boxes of a given type may always be subsumed into other bounding boxes of that
        type.

        @param box_to_be_subbed:    A Box object, which is to be subsumed.
        @return:                    A list of str values that describe which items that the current bounding box may be
                                    subsumed into.
        """
        list_of_items_can_sub_into: list = [box_to_be_subbed.label]
        if box_to_be_subbed.label in self.__items_to_sub__:
            list_of_items_can_sub_into.extend(self.__items_to_sub__[box_to_be_subbed.label])
        return list_of_items_can_sub_into

    def set_overlap_threshold(self, allowed_overlap=0.9):
        """
        A setter for the overlap threshold, above which bounding boxes are subsumed into each other.  If this proportion
        of a box overlaps another box (of an appropriate type) then the box will be subsumed into the other box.

        @param allowed_overlap: A float which is the minimum amount of overlap needed to subsume a bounding box into
                                another one.  Expressed as a decimal of the total area of the overlapping box.
        @return:
        """
        self.__overlap_threshold__ = allowed_overlap
