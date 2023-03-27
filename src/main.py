from model.Tracker import Tracker
from model.cv2wrapper import Display
from model.cv2wrapper.Detector import Detector
from model.cv2wrapper.Recorder import Recorder
from util.Debugging import debug_print, display_progress_percent


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")
        tracker = Tracker()
        detector_model = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
        # video_file = ".\\movie_002_2023-03-11"  # First Unity scene.
        video_file = ".\\tracker_test_video"  # Tracker test (living room chair).
        file_extension = ".mp4"
        with_bounding_boxes = "_with_bounding_boxes"

        # webcam_detector = Detector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")
        file_detector = Detector(detector_model, video_file+file_extension)

        detector = file_detector
        recorder = Recorder(file_name=video_file+with_bounding_boxes+file_extension, width=detector.get_frame_width(), height=detector.get_frame_height())

        keep_going = True
        while keep_going:
            if detector.try_loading_next_frame():
                detector.run_detection_on_current_frame(0.05)

                frame = detector.get_frame_with_bounding_boxes()
                Display.show(frame)  # Comment out to stop video display.
                recorder.add_frame(frame)  # Comment out to stop video recording.

                tracker.detect(detector.get_bounding_boxes())

                display_progress_percent(detector.get_current_frame_number(),
                                         detector.get_total_frame_count())
            else:
                keep_going = False

        Display.hide()
