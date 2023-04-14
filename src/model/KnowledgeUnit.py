from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box


class KnowledgeUnit:
    """
    A class to hold all functionality relating to drawing inferences from the detected bounding boxes, and for creating
    structured data which can be readily converted into output for the user.
    """

    def __init__(self):
        """
        The constructor for the class.
        """
        self.__impossible_items__: list = list()
        self.__recorded_items__: dict = dict()
        self.__facts__: KnowledgeUnit.Facts = KnowledgeUnit.Facts()
        self.__standard_strings__: KnowledgeUnit.StandardStrings = KnowledgeUnit.StandardStrings()
        self.__current_frame__: KnowledgeUnit.Frame | None = None
        self.__last_frame_time__: int = 0

    def get_list_of_all_seen_items(self) -> list:
        """
        Returns a list of all unique item types (as str values) that have been seen so far.

        @return: A list of all unique item types that have been seen so far.
        """
        return sorted(self.__recorded_items__.keys())

    def add_frame(self, frame_boxes: BoundingBoxCollection, time: int):
        """
        Add a new frame to the Unit.  Future queries about what items have been detected will be answered using the most
        recent frame data.

        @param frame_boxes: A BoundingBoxCollection which is the boxes detected in this frame.
        @param time:        An int which is the current time.  The units are not defined.
        @return:
        """

        frame_boxes.sort_by_area()
        frame: KnowledgeUnit.Frame = KnowledgeUnit.Frame(frame_boxes)
        self.__rename_impossible_items_in_frame__(frame)
        self.__current_frame__ = frame

        for i in range(len(frame.item_types)):
            item_name = frame.item_types[i]
            count = frame.item_counts[i]
            if item_name not in self.get_list_of_all_seen_items():
                self.__add_new_item__(item_name, count, time)
            elif item_name not in self.__impossible_items__:
                self.__update_existing_item_record__(item_name, count, time)

        self.__last_frame_time__ = time

    def __update_existing_item_record__(self, item_name: str, item_count_in_frame: int, time: int):
        """
        Updates the record of an item type which has already been seen.

        @param item_name:               A str which is the type of the item.
        @param item_count_in_frame:     An int which is how many times a particular item has been seen in this frame.
        @param time:                    An int which is the time this frame was recorded at.
        @return:
        """
        recorded_count, times = self.__recorded_items__[item_name]
        if item_count_in_frame > recorded_count:
            recorded_count = item_count_in_frame

        if times[-1] == self.__last_frame_time__:
            times[-1] = time
        else:
            times.append(time)

        self.__recorded_items__[item_name] = (recorded_count, times)

    def __rename_impossible_items_in_frame__(self, frame: 'KnowledgeUnit.Frame'):
        """
        Takes the stored Frame object and changes the names of any "impossible" items to the "unknown item" string.

        @param frame:   The KnowledgeUnit.Frame class to re-label impossible items in.
        @return:
        """
        for i in range(len(frame.item_types)):
            if frame.item_types[i] in self.__impossible_items__:
                frame.item_types[i] = self.__standard_strings__.unknown_item

    def __add_new_item__(self, item_name: str, item_count_in_frame: int, time: int):
        """
        When a new item category has been seen for the first time, this function generates a new record of that item
        category.

        @param item_name:               A str which is the name of the item category.
        @param item_count_in_frame:     An int which is the number of times this item was seen in this frame.
        @param time:                    An int which is the time this frame was recorded at.
        @return:
        """
        self.__recorded_items__[item_name] = (item_count_in_frame, [time])

    def how_many_have_you_seen(self, item_label: str) -> int:
        """
        Returns the highest number of this item type that has been seen in any one frame.

        @param item_label:  A str which is the item type that is being searched for.
        @return:            An int which is the maximum number of the given item that has been seen in any one frame.
        """
        for item_name in self.__recorded_items__.keys():
            if item_name == item_label:
                count, _ = self.__recorded_items__[item_name]
                return count
        return 0

    def when_did_you_see(self, item_name: str) -> list:
        """
        A getter for the times that a particular category of item has been seen.  Returns a list of times which
        correspond to the last times when a type of object was in frame.  If an object went out of frame, and was
        spotted again later, then the end time of both sightings will be returned in the list.

        The times are in whatever time units were passed in to the Knowledge Unit in the add_frame() function.

        @param item_name:   A str which is the item type to search for.
        @return:            A list which contains the integer times that the given object was last seen at.
        """
        if item_name in self.get_list_of_all_seen_items():
            _, times_seen = self.__recorded_items__[item_name]
            return times_seen
        return list()

    def where_did_you_see(self, item_name: str) -> list:
        """
        Returns a description of the location that the given item was last seen at.  This function is very much a work
        in progress, and at present only gives a list of either empty strings or strings saying "on the floor" if the
        item is known to not normally be on the floor.

        @param item_name:   A str which is the name of the item type to search for.
        @return:            A list of str values which describe the locations this item type has been seen in.
        """
        if item_name in self.get_list_of_all_seen_items():
            if item_name in self.__facts__.items_not_normally_on_floor:
                return [self.__standard_strings__.on_the_floor]
            return [self.__standard_strings__.empty_str]
        return list()

    def set_items_not_normally_on_floor(self, items: list):
        """
        Tells the Knowledge Unit that these items should not normally be found on the floor, which aids in describing
        item locations to the user.

        @param items: A list of str values which are the item categories that are not normally found on the floor.
        @return:
        """
        self.__facts__.items_not_normally_on_floor = items

    def set_impossible_items(self, items: list):
        """
        Tells the Knowledge Unit that these items are "impossible", and should not be reported to the user.  This is to
        help mitigate the problem of outlandish items being reported to the user from the object recognition software.

        @param items: A list of str values which are the item categories which should not be reported to the user.
        @return:
        """
        self.__impossible_items__ = items

    def describe_scene(self) -> dict:
        """
        used to get information with which to describe the current frame ot the user.  Returns a dict containing the
        in-scene items listed in three categories: left, centre, and right.  Custom category items which have been
        identified in the frame are also returned as lists in this dict.

        @return: A dict object which contains information with which to describe the scene to the user.
        """
        description = dict()
        items: BoundingBoxCollection = self.__current_frame__.bboxes
        items_ahead: list = list()
        items_left: list = list()
        items_right: list = list()

        for item in items:
            if self.__item_is_ahead__(item):
                items_ahead.append(item.label)
            if self.__item_is_left__(item):
                items_left.append(item.label)
            if self.__item_is_right__(item):
                items_right.append(item.label)

        description[self.__standard_strings__.ahead] = sorted(items_ahead)
        description[self.__standard_strings__.left] = sorted(items_left)
        description[self.__standard_strings__.right] = sorted(items_right)

        for custom_category in self.__facts__.custom_categories.keys():
            category_items: list = list()
            for item in items:
                if item.label in self.__facts__.custom_categories[custom_category]:
                    category_items.append(item.label)
            description[custom_category] = sorted(category_items)

        return description

    def __item_is_right__(self, item: Box) -> bool:
        """
        Works out if a given item is on the right hand side of a frame.

        @param item:    A Box object which is the item to assess.
        @return:        A bool which describes if this item is on the right hand side of the frame or not.
        """
        return item.right_edge > self.__facts__.right_frame_boundary

    def __item_is_left__(self, item: Box) -> bool:
        """
        Works out if a given item is on the left hand side of a frame.

        @param item:    A Box object which is the item to assess.
        @return:        A bool which describes if this item is on the left hand side of the frame or not.
        """
        return item.left_edge < self.__facts__.left_frame_boundary

    def __item_is_ahead__(self, item: Box) -> bool:
        """
        Works out if a given item is in the middle of the frame.

        @param item:    A Box object which is the item to assess.
        @return:        A bool which describes if this item is in the centre of the frame or not.
        """
        return item.right_edge > self.__facts__.left_frame_boundary \
            and item.left_edge < self.__facts__.right_frame_boundary

    def set_left_and_right(self, left_boundary: float, right_boundary: float):
        """
        Allows definition of the boundaries for where the left and right sides of a frame begin.  These currently
        default to 0.33 and 0.66 of the frame width.

        @param left_boundary:   A float which is the decimal of the frame with where the left edge of the frame begins.
        @param right_boundary:  A float which is the decimal of the frame with where the right edge of the frame begins.
        @return:
        """
        self.__facts__.left_frame_boundary = left_boundary
        self.__facts__.right_frame_boundary = right_boundary

    def set_custom_category(self, name: str, items: list):
        """
        Allows the setting of a custom category of objects.  This aids in providing descriptions of scenes and locations
        to the user.

        @param name:    A str which is the name of the new category.
        @param items:   A list of str values which are the names of items in the new category.
        @return:
        """
        self.__facts__.custom_categories[name] = items

    def get_list_of_seen_items_in_category(self, category: str) -> list:
        """
        Returns a list of all items seen in the given category.  The categories can be set using the
        set_custom_category() function.

        @param category:    A str which is the category name to search for.
        @return:            A list of str values which are the items from the category which have been seen.
        """
        seen_category_items: list = list()
        for item_name in self.get_list_of_all_seen_items():
            if item_name in self.__facts__.custom_categories[category]:
                seen_category_items.append(item_name)
        return seen_category_items

    def where_is(self, item_name: str) -> dict:
        """
        Returns information which can be used to describe where in the current scene an object is.  Please note that the
        behaviour of this function is undefined for cases where there are multiple occurrences of an item in a scene.

        @param item_name:   A str which is the name of the item to describe the location of.
        @return:            A dict which contains information that can be used to describe the location of an item to
                            the user.
        """
        item_location: dict = dict()
        frame_bboxes: BoundingBoxCollection = self.__current_frame__.bboxes

        for item in frame_bboxes:
            if item.label == item_name:
                item_location[self.__standard_strings__.direction] = self.__get_direction_list__(item)
                item_location[self.__standard_strings__.beneath] = self.__get_list_of_items_above_this__(item)
                item_location[self.__standard_strings__.on_top_of] = self.__get_on_top_of__(item)
                return item_location

        return item_location

    def __get_on_top_of__(self, item_on_top: Box) -> str:
        """
        Finds the name of the item which the given item is believed to be on top of, if any.  This can be used to help
        describe the scene to the user.

        @param item_on_top: A str which is the name of the item in the current frame which may be on top of something.
        @return:            A str which is the name ("" if none) of the item the given item is on top of.
        """
        object_item_is_on_top_of = self.__standard_strings__.empty_str
        if item_on_top.label in self.__facts__.furniture_items:
            return object_item_is_on_top_of

        max_area_below: float = 0.0
        frame_items: BoundingBoxCollection = self.__current_frame__.bboxes
        for item_below in frame_items:
            high_enough_to_sit_on = item_below.upper_edge + self.__facts__.max_gap_for_item_on_top_of_another
            if high_enough_to_sit_on > item_on_top.lower_edge:
                if item_below.left_edge < item_on_top.right_edge and item_below.right_edge > item_on_top.left_edge:
                    if item_below is not item_on_top:
                        area_below = item_below.get_overlap_area(Box(0.0, 1.0, 0.0, item_on_top.lower_edge, 1.0, ""))
                        if area_below > max_area_below:
                            max_area_below = area_below
                            object_item_is_on_top_of = item_below.label

        return object_item_is_on_top_of

    def __get_list_of_items_above_this__(self, item_beneath: Box) -> list:
        """
        Finds the names of any items the given object is believed to be beneath.  These objects are only the ones which
        have been classified as "wall and ceiling objects" in the add_wall_and_ceiling_objects() function.  Any other
        objects which appear above the target object in scene are assumed to be on the floor and therefore further away
        from the user than the target, rather than above the target.

        @param item_beneath:    A Box object which is the target item in the current frame to find items above.
        @return:                A list of str values which are the wall and ceiling items above the target item.
        """
        item_beneath_these_objects: list = list()

        frame_items: BoundingBoxCollection = self.__current_frame__.bboxes
        for item_above in frame_items:
            if item_above.label in self.__facts__.wall_and_ceiling_items:
                if item_above.lower_edge > item_beneath.lower_edge:
                    if item_above.right_edge > item_beneath.left_edge \
                            and item_above.left_edge < item_beneath.right_edge:
                        item_beneath_these_objects.append(item_above.label)

        return sorted(item_beneath_these_objects)

    def set_max_gap_for_item_on_top_of_another_item(self, max_gap: float):
        """
        Set the maximum vertical gap (measured as a decimal of the total frame height) between an item and the object
        (if any) that it will be described as resting on top of.  This exists to avoid objects on top of, for example, a
        table being erroneously described as being on the floor on the far side of the table, due to the tables bounding
        box being identified as being slightly smaller than it should be by the object identification system.

        @param max_gap: A float value which is the maximum gap (as a decimal of the frame height) between an item and
                        the item it will be described as being on top of.
        @return:
        """
        self.__facts__.max_gap_for_item_on_top_of_another = max_gap

    def add_wall_and_ceiling_objects(self, items: list):
        """
        Allows wall and ceiling items (relevant for the location descriptions given to the user) to be defined.

        @param items:     A list of str values, which are the item names to record as wall and ceiling items.
        @return:
        """
        self.__facts__.wall_and_ceiling_items = items

    def __get_direction_list__(self, item: Box) -> list:
        """
        Returns a list which contains one or more str values, which describes whether the target item is to the left,
        ahead, or to the right in the current frame.

        @param item:    A Box object, which is the item to get the direction of.
        @return:        A list of str values, which describe the directions the target item can be found in.
        """
        direction: list = list()
        if self.__item_is_ahead__(item):
            direction.append(self.__standard_strings__.ahead)
        if self.__item_is_left__(item):
            direction.append(self.__standard_strings__.left)
        if self.__item_is_right__(item):
            direction.append(self.__standard_strings__.right)
        return sorted(direction)

    def set_furniture_items(self, furniture_items: list):
        """
        Allows definition of a list of items which will not be displayed as being on top of another item.  This is to
        reduce the chances of, for example, chairs on the far side of a table being erroneously described as being on
        top of the table.

        @param furniture_items: A list of str values, which are the names of items of furniture.
        @return:
        """
        self.__facts__.furniture_items = furniture_items

    def items_between_user_and(self, item_name: str) -> list:
        """
        Returns a list of all items in the current frame which are in-between the user and the target item.  Please note
        that "in-between" is defined as any item that has a lower edge in the current frame than the target item (as
        this should mean that it is closer to the user), and that no effort is made ot determine if an item is not
        actually on a direct line between the user and the target.  This is to avoid mistakes in the system erroneously
        describing there being no intervening items to a user.  Please also note that the behaviour of this function is
        undefined for instances where there are multiple instances of the target item in the current frame.

        @param item_name:   The name of the target item.
        @return:            A list of str values which are the names of items which may be in-between the user and the
                            target.
        """
        for item in self.__current_frame__.bboxes:
            if item.label == item_name:
                return self.__get_intervening_items__(item)

        return list()

    def __get_intervening_items__(self, target_item: Box) -> list:
        """
        Returns a list of all items in the given frame which are in-between (see definition in the
        items_between_user_and() function) the target and the user.

        @param target_item: A Box object which is the target.
        @return:            A list of str values which are the names of items which may be in-between the user and the
                            target.
        """
        intervening_items: list = list()

        for intervening_item in self.__current_frame__.bboxes:
            if intervening_item.lower_edge < target_item.lower_edge \
                    and intervening_item is not target_item:
                intervening_items.append(intervening_item.label)

        return intervening_items

    class StandardStrings:
        """
        A simple struct class to hold all of the text strings that may be returned to the user.  The point of this class
        is to make it easier to alter the strings throughout the program, particularly the strings that are used as dict
        keys.  This could also be used in a language/localisation system in the future.
        """

        def __init__(self):
            """
            The constructor for the class.  Defines all the str values which may be used.
            """
            self.unknown_item: str = "unknown item"
            self.on_the_floor: str = "on the floor"
            self.ahead: str = "ahead"
            self.left: str = "left"
            self.right: str = "right"
            self.direction = "direction"
            self.beneath = "beneath"
            self.on_top_of = "on top of"
            self.empty_str = ""

    class Frame:
        """
        A class to hold data about a particular frame, which can then be easily accessed by the parent class.
        """
        def __init__(self, bboxes: BoundingBoxCollection):
            """
            The class constructor.  Takes in a collection of the bounding boxes which were identified in the frame, and
            then generates some useful summary data about the frame which can be readily accessed by the parent class.

            @param bboxes:  A BoundingBoxCollection object which contains the bounding boxes identified in the frame.
            """
            self.bboxes: BoundingBoxCollection = bboxes
            self.item_types: list = list()
            self.item_counts: list = list()

            for box in bboxes:
                label = box.label
                if label not in self.item_types:
                    self.item_types.append(label)
                    self.item_counts.append(1)
                else:
                    index = self.item_types.index(label)
                    self.item_counts[index] += 1

    class Facts:
        """
        A simple struct class to hold all the data which is "known" about the world, and is used to describe the scene
        to a user.
        """
        def __init__(self):
            """
            The constructor for the class.  Initialises the default values for all "facts".
            """
            self.items_not_normally_on_floor: list = list()
            self.wall_and_ceiling_items: list = list()
            self.furniture_items: list = list()
            self.left_frame_boundary = 0.33
            self.right_frame_boundary = 0.66
            self.custom_categories: dict = dict()
            self.max_gap_for_item_on_top_of_another: float = 0.0
