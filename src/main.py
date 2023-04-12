import sys

from cv2wrapper.Frame import Frame
from model.KnowledgeUnit import KnowledgeUnit
from model.SubsumptionUnit import SubsumptionUnit
from model.Tracker import Tracker
from cv2wrapper.Display import Display
from cv2wrapper.Detector import Detector
from cv2wrapper.Recorder import Recorder
from util.Debugging import display_progress_percent


class MainClass:
    if __name__ == "__main__":
        print("Main class running!")

        # Set up Tracker
        tracker = Tracker(min_frames=20, allowed_absence=20, iou_threshold=0.7)

        # Set up Knowledge Unit
        knowledge = KnowledgeUnit()
        knowledge.set_impossible_items([])

        # Set up Subsumption Unit
        sub_unit = SubsumptionUnit()
        sub_unit.set_overlap_threshold(0.7)
        sub_unit.add_list(["Book case", "Shelf"])
        sub_unit.add_list(["Chair", "Table", "Shelf", "Footwear"])
        sub_unit.add_list(["Person", "Clothing", "Human face", "Human leg"])
        sub_unit.add_list(["Clothing", "Footwear"])

        # Set up CV2 Wrapper classes.
        detector_model = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
        # video_file = ".\\movie_002_2023-03-11"  # First Unity scene.
        video_file = ".\\..\\Videos\\tracker_test_video"  # Tracker test (living room chair).
        file_extension = ".mp4"
        with_bounding_boxes = "_with_bounding_boxes"
        # webcam_detector = Detector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")
        file_detector = Detector(detector_model, video_file + file_extension)
        detector = file_detector
        detector.set_perform_nms(False)  # Set to not perform NMS so s not to interfere with the Subsumption Unit
        detector.set_detection_confidence_threshold(0.1)
        detector.set_nms_overlap_threshold(0.1)
        detector.set_nms_eta_parameter(None)
        detector.set_nms_top_k_parameter(None)

        display = Display()
        recorder = Recorder(file_name=video_file + with_bounding_boxes,
                            width=detector.get_frame_width(),
                            height=detector.get_frame_height())

        keep_going = True
        paused = False
        key_pressed: str | None = None
        frames_per_sec = detector.get_fps()
        secs_per_frame = 1 / frames_per_sec
        while keep_going:
            if not paused:
                if detector.try_loading_next_frame():
                    # Calculate video time.
                    time: int = round(detector.get_current_frame_number() * secs_per_frame)

                    # Get all data from the Detector.
                    detector.run_detection_on_current_frame()
                    frame: Frame = detector.get_frame()
                    detected_items = detector.get_bounding_boxes()

                    # Process the data before handing over to the logic units.
                    detected_items.trim_by_confidence(min_confidence=0.1)
                    detected_items = sub_unit.subsume_bboxes(detected_items)

                    # Generate tracks and pass them to the Knowledge Unit.
                    tracker.add_new_frame(detected_items)
                    current_tracks, track_ids = tracker.get_current_tracks()
                    knowledge.add_frame(current_tracks, time)

                    # Housekeeping Functions.
                    frame.draw_bounding_boxes(current_tracks)  # Show items being tracked.
                else:
                    keep_going = False

            # Housekeeping functions.
            key_pressed = display.show(frame)  # Comment out to stop video display.
            recorder.add_frame(frame)  # Comment out to stop video recording.
            display_progress_percent(detector.get_current_frame_number(), detector.get_total_frame_count())

            # Handle any key presses:
            if key_pressed == ord('z'):
                print(knowledge.get_list_of_all_seen_items())
            elif key_pressed == ord(' '):
                paused = not paused
            elif key_pressed == 'q':
                sys.exit()  # Doesn't work for some reason.


