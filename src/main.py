from model.Model import Model
from model.cv2wrapper import Display
from model.cv2wrapper.Detector import Detector


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")
        model = Model()

        window_name = 'AILSA System'
        webcam_detector = Detector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")
        file_detector = Detector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1",
                                 "C:\\Users\\hughm\\Desktop\\Written_Code\\Ailsa\\movie_002_2023-03-11.mp4")
        detector = file_detector

        keep_going = True
        while keep_going:
            frame, bounding_boxes = detector.get_frame_with_boxes()
            model.detect(bounding_boxes)
            keep_going = Display.show(frame)
        Display.hide()
