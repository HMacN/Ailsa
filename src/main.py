from cv2wrapper.Frame import Frame
from model.SubsumptionUnit import SubsumptionUnit
from model.Tracker import Tracker
from cv2wrapper.Display import Display
from cv2wrapper.Detector import Detector
from cv2wrapper.Recorder import Recorder
from util.Debugging import display_progress_percent


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")
        tracker = Tracker(min_frames=20, allowed_absence=20)
        sub_unit = SubsumptionUnit()
        detector_model = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
        # video_file = ".\\movie_002_2023-03-11"  # First Unity scene.
        video_file = ".\\..\\Videos\\tracker_test_video"  # Tracker test (living room chair).
        file_extension = ".mp4"
        with_bounding_boxes = "_with_bounding_boxes"

        # webcam_detector = Detector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")
        file_detector = Detector(detector_model, video_file + file_extension)

        display = Display()
        detector = file_detector

        detector.set_detection_confidence_threshold(0.1)
        detector.set_nms_overlap_threshold(0.1)
        detector.set_nms_eta_parameter(None)
        detector.set_nms_top_k_parameter(None)

        recorder = Recorder(file_name=video_file + with_bounding_boxes,
                            width=detector.get_frame_width(),
                            height=detector.get_frame_height())

        keep_going = True
        while keep_going:
            if detector.try_loading_next_frame():
                detector.run_detection_on_current_frame()

                frame: Frame = detector.get_frame()
                detected_items = detector.get_bounding_boxes()
                tracker.add_new_frame(detector.get_bounding_boxes())
                current_tracks, track_ids = tracker.get_current_tracks()
                frame.draw_bounding_boxes(current_tracks)

                display.show(frame)  # Comment out to stop video display.
                recorder.add_frame(frame)  # Comment out to stop video recording.

                display_progress_percent(detector.get_current_frame_number(),
                                         detector.get_total_frame_count())
            else:
                keep_going = False

        display.hide()
