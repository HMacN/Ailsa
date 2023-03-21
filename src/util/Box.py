class Box:

    def __init__(self, left_edge: float, right_edge: float,
                 lower_edge: float, upper_edge: float, confidence: float, label: str):
        self.left_edge: float = left_edge
        self.right_edge: float = right_edge
        self.lower_edge: float = lower_edge
        self.upper_edge: float = upper_edge
        self.confidence: float = confidence
        self.label: str = label

    def __str__(self) -> str:
        left = "left: " + str(self.left_edge)
        right = "right: " + str(self.right_edge)
        lower = "lower: " + str(self.lower_edge)
        upper = "upper: " + str(self.upper_edge)
        conf = "conf: " + str(self.confidence)
        label = "label: " + str(self.label)
        c = ", "

        return left + c + right + c + lower + c + upper + c + conf + c + label
