from controller import IController
from controller.Controller import Controller
from model import IModel
from model.Model import Model
from view import IView
from view.View import View


class MainClass:
    model: IModel = Model()
    view: IView = View()
    controller: IController = Controller()

    def __init__(self):
        pass

    if __name__ == "__main__":
        print("Main class running!")
