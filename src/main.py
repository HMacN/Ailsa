from model.Model import Model
from util.ObjectRecognition.TFlow import TFlow


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")
        model = Model()

        tf = TFlow()
        tf.go()

