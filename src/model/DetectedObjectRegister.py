from util.IdentifiedObject import IdentifiedObject


class DetectedObjectRegister:

    def __init__(self):
        self.__list_of_items = list()

    def add(self, item: IdentifiedObject):

        if item not in self.__list_of_items:
            self.__list_of_items.append(item)

    def get_by_name(self, name: str) -> list:

        list_to_return = list()

        for i in range(len(self.__list_of_items)):
            if self.__list_of_items[i].get_object_name() == name:
                list_to_return.append(self.__list_of_items[i])

        return list_to_return
