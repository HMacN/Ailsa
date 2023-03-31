import cv2
import tensorflow_hub as hub
import tensorflow as tf

from cv2wrapper.Frame import Frame
from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box
from util.Debugging import debug_print


class Detector:

    def __init__(self, model_url: str, file_path=0):
        self.__model__ = hub.load(model_url).signatures['default']
        self.__video_capture__ = cv2.VideoCapture(file_path)
        self.__current_frame__: Frame | None = None
        self.__current_bounding_boxes__: BoundingBoxCollection | None = None

    def try_loading_next_frame(self) -> bool:
        try:
            _, frame = self.__video_capture__.read()
            self.__current_frame__ = Frame.new_from_cv2(frame)
            has_next_frame = self.__current_frame__ is not None
        except cv2.error:
            has_next_frame = False

        return has_next_frame

    def run_detection_on_current_frame(self):
        detection_results = self.__get_detection_results__()

        bounding_boxes = self.__convert_cv2_results_to_bounding_box_collection__(detection_results)

        self.__current_bounding_boxes__ = bounding_boxes

    def get_frame(self) -> Frame:
        return self.__current_frame__

    def get_bounding_boxes(self) -> BoundingBoxCollection:
        return self.__current_bounding_boxes__

    def __get_detection_results__(self):
        converted_img = tf.image.convert_image_dtype(self.__current_frame__.get_cv2_img(), tf.float32)[tf.newaxis, ...]
        results = self.__model__(converted_img)
        results = {key: value.numpy() for key, value in results.items()}
        return results

    def get_frame_width(self) -> int:
        if self.__video_capture__ is None:
            return 0
        else:
            width = self.__video_capture__.get(cv2.CAP_PROP_FRAME_WIDTH)
            return int(width)

    def get_frame_height(self) -> int:
        if self.__video_capture__ is None:
            return 0
        else:
            height = self.__video_capture__.get(cv2.CAP_PROP_FRAME_HEIGHT)
            return int(height)

    def __get_progress_percent__(self) -> int:
        cap = self.__video_capture__
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        progress_decimal = current_frame / total_frames
        return int(progress_decimal * 100)

    def get_total_frame_count(self) -> int:
        if self.__video_capture__ is None:
            return 0
        else:
            return self.__video_capture__.get(cv2.CAP_PROP_FRAME_COUNT)

    def get_current_frame_number(self):
        if self.__video_capture__ is None:
            return 0
        else:
            return self.__video_capture__.get(cv2.CAP_PROP_POS_FRAMES)

    @staticmethod
    def __convert_cv2_results_to_bounding_box_collection__(detection_results) -> BoundingBoxCollection:
        number_of_boxes = len(detection_results["detection_boxes"])
        boxes = BoundingBoxCollection()

        for i in range(number_of_boxes):
            new_box = Box(left_edge=detection_results["detection_boxes"][i][1],
                          right_edge=detection_results["detection_boxes"][i][3],
                          lower_edge=detection_results["detection_boxes"][i][0],
                          upper_edge=detection_results["detection_boxes"][i][2],
                          confidence=detection_results["detection_scores"][i],
                          label=detection_results["detection_class_entities"][i])
            boxes.add(new_box)

        return boxes
