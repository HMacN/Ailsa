from util.Box import Box


class BoxList:
    """
    A wrapper class for a Python list() containing Box objects.  This class exists to hold a series of commonly used
    functions for manipulating the lists of Box objects.
    """
    def __init__(self):
        """
        The constructor.  Initialises the object with an empty list of boxes.
        """
        self.__boxes__: list = list()

    def __str__(self) -> str:
        """
        An override of the __str__() function.  Provides a readable string of all the contained data.  Two objects which
        contain the same data will have identical strings.

        @return: A str value which summarises the contents of this object.
        """
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
        """
        An override of the __eq__() function.  This uses the __str__() function to check for equality between two
        collections that contain the same data.  I.e. if the collections contain the same boxes then they will be listed
        as equal.

        @param other:   The other object to check for equality.
        @return:        A bool which describes if the given object is equal to this one.
        """
        if not isinstance(other, self.__class__):
            return False

        self_str = str(self)
        other_str = str(other)

        if self_str != other_str:
            return False

        return True

    def add(self, box: Box):
        """
        Add a box to the collection.

        @param box: A Box object to add to the collection.
        @return:
        """
        self.__boxes__.append(box)

    def get(self, index: int) -> Box | None:
        """
        A getter for the box at the given index.  Returns None if the index is invalid for any reason.

        @param index:   An int which is the index of the box to return.
        @return:        A Box object, which is the box at the given index.
        """
        if index < 0 or index >= len(self.__boxes__):
            return None

        return self.__boxes__[index]

    def sort_by_confidence(self):
        """
        Sorts the collection in descending order of detection confidence.

        @return:
        """
        def k(box: Box):
            return box.confidence

        self.__boxes__.sort(key=k, reverse=True)

    def trim_by_confidence(self, min_confidence: float):
        """
        Removes all the boxes in the collection that have a detection confidence below the given minimum.

        @param min_confidence:  A float which is the minimum confidence level to keep.
        @return:
        """

        boxes_to_remove = list()

        for box in self.__boxes__:
            if box.confidence < min_confidence:
                boxes_to_remove.append(box)

        for box_to_remove in boxes_to_remove:
            self.__boxes__.remove(box_to_remove)

    def size(self):
        """
        A getter for the size (number of boxes contained) in this collection.

        @return: An int which is the number of boxes contained.
        """
        return len(self.__boxes__)

    def contains(self, box: Box) -> bool:
        """
        Checks if a given box is present in the collection.

        @param box: A Box object which is the box to search for in the collection.
        @return:    A bool which states whether or not the given box was found in the collection.
        """
        return box in self.__boxes__

    def pop(self, index: int) -> Box:
        """
        Remove and return the box at the given index.

        @param index:   The index of the box to remove and return.
        @return:        A Box object, which is the box removed from the given index.
        """
        return self.__boxes__.pop(index)

    def __iter__(self) -> 'BoxList':
        """
        Override of the iter function, which allows the collection to be used like a normal list.

        @return: A BoxList object, which is the iterable object.
        """
        self.iter_value = 0
        return self

    def __next__(self) -> Box:
        """
        Override of the iter function, which allows the collection to be used like a normal list.

        @return: A Box object, which is the next object in the collection.
        """
        if self.iter_value < self.size():
            box = self.__boxes__[self.iter_value]
            self.iter_value += 1
            return box
        else:
            raise StopIteration

    def __getitem__(self, key) -> Box:
        """
        Override of the getitem function, which allows the collection to be used like a normal list.

        @param key:     An int, which is the index of the box to get.
        @return:        A Box object, which is the box at the given index.
        """
        return self.__boxes__[key]

    def __setitem__(self, key: int, value: Box):
        """
        Override of the setitem function, which allows the collection to be used like a normal list.

        @param key:     An int, which is the index at which to replace a box.
        @param value:   A Box object, which is the box to replace an existing box with.
        @return:
        """
        self.__boxes__[key] = value

    def __delitem__(self, key: int):
        """
        Override of the delitem function, which allows the collection to be used like a normal list.

        @param key:     An int, which is the index of the box to delete.
        @return:
        """
        del self.__boxes__[key]

    def remove(self, box: Box):
        """
        Removes the first occurrence of the given box from the collection.

        @param box: A Box object which is to be removed from the collection.
        @return:
        """
        self.__boxes__.remove(box)

    def __len__(self) -> int:
        """
        Override of the len function, which allows the collection to be used like a normal list.

        @return: An int, which is the number of boxes in the collection.
        """
        return len(self.__boxes__)

    def sort_by_area(self):
        """
        Sorts the collection in descending order of box area.

        @return:
        """
        def foo(e: Box):
            return e.get_area()

        self.__boxes__.sort(key=foo)
