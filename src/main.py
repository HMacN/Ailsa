from controller import IController
from model import IModel
from util.ObjectRecognition.TFlow import TFlow
from util.Starter import Starter
from view import IView


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")
        starter: Starter = Starter()

        model: IModel = starter.get_model()
        view: IView = starter.get_view()
        controller: IController = starter.get_controller()

        tf = TFlow()
        tf.go()

