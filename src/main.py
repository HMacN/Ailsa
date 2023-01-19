from controller import IController
from controller.Controller import Controller
from model import IModel
from model.Model import Model
from view import IView
from view.View import View


class MainClass:

    def __init__(self):
        self.model: IModel = None
        self.view: IView = None
        self.controller: IController = None

    if __name__ == "__main__":
        print("Main class running!")
