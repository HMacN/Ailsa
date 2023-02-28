from model.DetectedObjectRegister import DetectedObjectRegister


class Model:

    def __init__(self):
        self.__register: DetectedObjectRegister = DetectedObjectRegister()

    def detect(self, items: list):
        for i in items:
            self.__register.add(i)

    def get_detected_items(self):
        return self.__register.get_all()
