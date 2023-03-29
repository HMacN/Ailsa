from util.Box import Box


class BoundingBoxCollection:
    def __init__(self):
        self.__boxes__: list = list()

    def __str__(self) -> str:
        string = ""
        box_ = "Box "
        _open_bracket_ = ": ["
        _close_bracket = "]"
        _new_line_ = "\n"

        for i in range(self.size()):
            string = string + box_ + str(i) + _open_bracket_ + str(self.__boxes__[i]) + _close_bracket

            if i != (self.size() - 1):
                string = string + _new_line_

        return string

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        self_str = str(self)
        other_str = str(other)

        if self_str != other_str:
            return False

        return True

    def add(self, box: Box):
        self.__boxes__.append(box)

    def get(self, index: int) -> Box | None:
        if index < 0 or index >= len(self.__boxes__):
            return None

        return self.__boxes__[index]

    def sort_by_confidence(self):
        def k(box: Box):
            return box.confidence

        self.__boxes__.sort(key=k, reverse=True)

    def trim_by_confidence(self, min_confidence: float):
        for box in self.__boxes__:
            if box.confidence < min_confidence:
                self.__boxes__.remove(box)

    def size(self):
        return len(self.__boxes__)
