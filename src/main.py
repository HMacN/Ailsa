from model.Model import Model
from model.cv2wrapper import Display
from model.cv2wrapper.Detector import Detector


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")
        model = Model()

        window_name = 'AILSA System'
        webcam_detector = Detector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")
        detector = webcam_detector

        keep_going = True
        while keep_going:
            keep_going = Display.show(detector.get_frame_with_boxes())
        Display.hide()
