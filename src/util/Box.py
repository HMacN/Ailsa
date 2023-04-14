

def __get_as_str__(string) -> str:
    """
    A helper function to make sure that a given string is in str format, and not a bytestring.

    @param string:  A string that may or may not be a bytestring.
    @return:        A str, which is the same as the given string.
    """
    if isinstance(string, (bytes, bytearray)):
        return str(string, "utf-8")
    elif isinstance(string, str):
        return string
    else:
        return str(string)


class Box:
    """
    A class to describe a single bounding box, along with some details and helpful functions.
    """

    def __init__(self, left_edge: float, right_edge: float,
                 lower_edge: float, upper_edge: float, confidence: float, label: str):
        """
        The constructor.

        @param left_edge:   A float, which is the left edge, expressed as a decimal of the width of the frame.
        @param right_edge:  A float, which is the right edge, expressed as a decimal of the width of the frame.
        @param lower_edge:  A float, which is the lower edge, expressed as a decimal of the height of the frame.
        @param upper_edge:  A float, which is the upper edge, expressed as a decimal of the height of the frame.
        @param confidence:  A float, which is the detection confidence, on a scale of 0.0 (doubt) to 1.0 (certainty).
        @param label:       A str, which is the classification of this item.
        """
        self.left_edge: float = left_edge
        self.right_edge: float = right_edge
        self.lower_edge: float = lower_edge
        self.upper_edge: float = upper_edge
        self.confidence: float = confidence
        self.label: str = __get_as_str__(label)

    def __str__(self) -> str:
        """
        An override of the str function.  Returns a string which summarises the contents of the box.

        @return:    A str which summarises the contents of the box.
        """
        left = "left: " + str(self.left_edge)
        right = "right: " + str(self.right_edge)
        lower = "lower: " + str(self.lower_edge)
        upper = "upper: " + str(self.upper_edge)
        conf = "conf: " + str(self.confidence)
        label = "label: " + str(self.label)
        c = ", "

        return left + c + right + c + lower + c + upper + c + conf + c + label

    def get_overlap_area(self, overlapping_box: 'Box') -> float:
        """
        Returns the absolute overlap area that this box shares with another box.  Returns 0.0 if the boxes do not
        overlap.

        @param overlapping_box: A Box object that this box may overlap with.
        @return:                A float which is the overlap area between the two boxes.
        """
        no_overlap = 0.0

        if self.left_edge > overlapping_box.right_edge:
            return no_overlap
        elif self.right_edge < overlapping_box.left_edge:
            return no_overlap
        elif self.lower_edge > overlapping_box.upper_edge:
            return no_overlap
        elif self.upper_edge < overlapping_box.lower_edge:
            return no_overlap

        overlap_upper_edge = min(self.upper_edge, overlapping_box.upper_edge)
        overlap_lower_edge = max(self.lower_edge, overlapping_box.lower_edge)
        overlap_left_edge = max(self.left_edge, overlapping_box.left_edge)
        overlap_right_edge = min(self.right_edge, overlapping_box.right_edge)

        overlap_area = (overlap_upper_edge - overlap_lower_edge) * (overlap_right_edge - overlap_left_edge)

        return overlap_area

    def get_iou(self, other_box: 'Box') -> float:
        """
        Returns the Intersection over Union factor for this box and the given box.  This is a commonly used metric in
        image detection systems.  Returns 0.0 if the boxes do not overlap.

        @param other_box:   A Box object with which to get the IoU factor of this box with.
        @return:            A float, which is the IoU factor of the given box with this one.
        """
        intersection_area = self.get_overlap_area(other_box)

        # Save time here by returning 0 if intersection area is effectively zero.
        if intersection_area < 0.0000001:
            return 0.0

        other_box_area = (other_box.right_edge - other_box.left_edge) * (other_box.upper_edge - other_box.lower_edge)
        union_area = self.get_area() + other_box_area - intersection_area

        intersection_over_union = intersection_area / union_area

        return intersection_over_union

    def get_area(self) -> float:
        """
        Gets the area of the box.

        @return: A float, which is the area of this box.
        """
        return (self.right_edge - self.left_edge) * (self.upper_edge - self.lower_edge)

