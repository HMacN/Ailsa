from model.Model import Model
from util.ObjectRecognition.TFlow import TFlow


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")
        model = Model()

        tf = TFlow()
        tf.go("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "C:/Users/hughm/Desktop/Written_Code/Ailsa/virtual_living_room.jpg")
