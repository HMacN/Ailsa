from util.Debugging import debug_print


def __get_as_str__(string):
    if isinstance(string, (bytes, bytearray)):
        return str(string, "utf-8")
    elif isinstance(string, str):
        return string
    else:
        return str(string)


class Box:

    def __init__(self, left_edge: float, right_edge: float,
                 lower_edge: float, upper_edge: float, confidence: float, label: str):
        self.left_edge: float = left_edge
        self.right_edge: float = right_edge
        self.lower_edge: float = lower_edge
        self.upper_edge: float = upper_edge
        self.confidence: float = confidence
        self.label: str = __get_as_str__(label)

    def __str__(self) -> str:
        left = "left: " + str(self.left_edge)
        right = "right: " + str(self.right_edge)
        lower = "lower: " + str(self.lower_edge)
        upper = "upper: " + str(self.upper_edge)
        conf = "conf: " + str(self.confidence)
        label = "label: " + str(self.label)
        c = ", "

        return left + c + right + c + lower + c + upper + c + conf + c + label

    def get_overlap_area(self, overlapping_box: 'Box') -> float:
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
        intersection_area = self.get_overlap_area(other_box)

        # Save time here by returning 0 if intersection area is effectively zero.
        if intersection_area < 0.0000001:
            return 0.0

        other_box_area = (other_box.right_edge - other_box.left_edge) * (other_box.upper_edge - other_box.lower_edge)
        union_area = self.get_area() + other_box_area - intersection_area

        intersection_over_union = intersection_area / union_area

        return intersection_over_union

    def get_area(self) -> float:
        return (self.right_edge - self.left_edge) * (self.upper_edge - self.lower_edge)

