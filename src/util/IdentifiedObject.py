from util.DebugPrint import debug_print


class IdentifiedObject:
    horizontal_distance_to_origin: int = None
    vertical_distance_to_origin: int = None
    bounding_box_width: int = None
    bounding_box_height: int = None
    object_name: str = None

    def __init__(self,
                 horizontal_distance_to_origin: int,
                 vertical_distance_to_origin: int,
                 bounding_box_width: int,
                 bounding_box_height: int,
                 object_name: str):
        self.horizontal_distance_to_origin: int = horizontal_distance_to_origin
        self.vertical_distance_to_origin: int = vertical_distance_to_origin
        self.bounding_box_width: int = bounding_box_width
        self.bounding_box_height: int = bounding_box_height
        self.object_name: str = object_name

    def __eq__(self, other):
        if isinstance(other, IdentifiedObject):

            names_the_same: bool = False
            numbers_the_same: bool = False

            if other.object_name == self.object_name:
                names_the_same = True

            if other.bounding_box_height == self.bounding_box_height & \
                    other.bounding_box_width == self.bounding_box_width & \
                    other.vertical_distance_to_origin == self.vertical_distance_to_origin & \
                    other.horizontal_distance_to_origin == self.horizontal_distance_to_origin:
                numbers_the_same = True

            if names_the_same & numbers_the_same:
                return True
            else:
                return False

    def __lt__(self, other):
        return self.object_name < other.object_name

    def get_horizontal_distance_to_origin(self):
        return self.horizontal_distance_to_origin

    def get_vertical_distance_to_origin(self):
        return self.vertical_distance_to_origin

    def get_bounding_box_width(self):
        return self.bounding_box_width

    def get_bounding_box_height(self):
        return self.bounding_box_height

    def get_object_name(self):
        return self.object_name
