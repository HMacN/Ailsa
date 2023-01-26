from util.IdentifiedObject import IdentifiedObject


class DetectedObjectRegister:

    def __init__(self):
        self.__list_of_items = list()

    def add(self, item: IdentifiedObject):
        self.__list_of_items.append(item)

    def get_by_name(self, name: str) -> list:
        return self.__list_of_items.copy()
