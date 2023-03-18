import cv2

from model.Model import Model
from model.cv2wrapper import Display
from model.cv2wrapper.Detector import Detector
from model.cv2wrapper.Recorder import Recorder
from util.DebugPrint import debug_print


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")
        model = Model()

        window_name = 'AILSA System'
        # webcam_detector = Detector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")
        file_detector = Detector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1",
                                 "C:\\Users\\hughm\\Desktop\\Written_Code\\Ailsa\\movie_002_2023-03-11.mp4")

        detector = file_detector
        detector.load_next_frame()
        first_frame, _ = detector.get_frame_with_boxes(0.05)
        Display.show(first_frame)

        recorder = Recorder("C:\\Users\\hughm\\Desktop\\Written_Code\\Ailsa\\",
                            "test_video",
                            detector.get_frame_width(),
                            detector.get_frame_height())

        keep_going = True
        while keep_going:
            if detector.load_next_frame() and not(Display.closed_by_user()):
                frame, bounding_boxes = detector.get_frame_with_boxes(0.05)
                recorder.add_frame(frame)
                model.detect(bounding_boxes)
                Display.show(frame)
            else:
                keep_going = False
        debug_print("Detected Items: ", model.get_detected_items())
        Display.hide()
