import cv2
import tensorflow_hub as hub
import tensorflow as tf

from cv2wrapper.Frame import Frame
from util.BoxList import BoxList
from util.Box import Box


class Detector:
    """
    A wrapper class for the OpenCV2 VideoCapture class, and the associated TensorFlowHub model.  This class provides an
    easier to use API, and converts the cv2 format object detection data into a BoxList object.
    """

    def __init__(self, model_url: str, file_path: str):
        """
        The constructor function for the class.  Sets up a TensorFlowHub model and a cv2.VideoCapture object.

        @param model_url A str which is the URL of the TensorFlowHub model to download and use.
        @param file_path A str which is the file path of the video file to run detection on.  Note that entering an
                'int' value will run object detection on the output from that number of webcam on the current device.
        """
        self.__should_perform_nms__ = True
        self.__model__ = hub.load(model_url).signatures['default']
        self.__video_capture__ = cv2.VideoCapture(file_path)
        self.__current_frame__: Frame | None = None
        self.__current_bounding_boxes__: BoxList | None = None

        self.__detection_confidence_threshold__: float = 0.1
        self.__nms_overlap_threshold__: float = 0.1
        self.__nms_eta__: float | None = None
        self.__nms_keep_top_k_indices__: float | None = None

    def try_loading_next_frame(self) -> bool:
        """
        A function to be called inside the main loop of a program.  Attempts to read the next frame from the
        VideoCapture object and updates the currently stored frame if successful.

        @return: A bool which indicates whether or not a new frame was successfully loaded.
        """
        try:
            _, frame = self.__video_capture__.read()
            self.__current_frame__ = Frame.new_from_cv2(frame)
            has_next_frame = self.__current_frame__ is not None
        except cv2.error:
            has_next_frame = False

        return has_next_frame

    def run_detection_on_current_frame(self):
        """
        Performs object detection on the current stored frame.  Updates the stored bounding boxes with the new results.

        @return:
        """
        detection_results = self.__get_detection_results__()

        bounding_boxes = self.__convert_cv2_results_to_bounding_box_collection__(detection_results)

        self.__current_bounding_boxes__ = bounding_boxes

    def __get_detection_results__(self) -> dict:
        """
        Actually performs the image detection, and returns the results in the CV2 data format.

        @return: A dict which is the detection results in the CV2 data format.
        """
        converted_img = tf.image.convert_image_dtype(self.__current_frame__.get_cv2_img(), tf.float32)[tf.newaxis, ...]
        results = self.__model__(converted_img)
        results = {key: value.numpy() for key, value in results.items()}

        if self.__should_perform_nms__:
            results = self.__perform_nms__(results)

        return results

    @staticmethod
    def __convert_cv2_results_to_bounding_box_collection__(detection_results: dict) -> BoxList:
        """
        Converts the CV2 format detection results into an easier to use form.

        @param detection_results: A dict which is the CV2 format detection results to be converted.
        @return: A BoxList which is the reformatted detection results.
        """

        boxes = BoxList()

        for i in range(len(detection_results["detection_boxes"])):
            new_box = Box(left_edge=detection_results["detection_boxes"][i][1],
                          right_edge=detection_results["detection_boxes"][i][3],
                          lower_edge=detection_results["detection_boxes"][i][0],
                          upper_edge=detection_results["detection_boxes"][i][2],
                          confidence=detection_results["detection_scores"][i],
                          label=detection_results["detection_class_entities"][i])
            boxes.add(new_box)

        return boxes

    def get_frame(self) -> Frame:
        """
        A getter for the current 'Frame' object.

        @return: A Frame object which represents the currently stored frame.
        """
        return self.__current_frame__

    def get_bounding_boxes(self) -> BoxList:
        """
        A getter for the most recent set of bounding boxes found by the Detector.  This corresponds to the results
        gained from the last time the 'run_detection_on_current_frame()' function was run.

        @return: A BoxList object which contains the bounding boxes identified in the most recent frame.
        """
        return self.__current_bounding_boxes__

    def get_frame_width(self) -> int:
        """
        A getter for the width of the frames of the video feed, in pixels.

        @return: An int which is the width of the video feed frames in pixels.
        """
        if self.__video_capture__ is None:
            return 0
        else:
            width = self.__video_capture__.get(cv2.CAP_PROP_FRAME_WIDTH)
            return int(width)

    def get_frame_height(self) -> int:
        """
        A getter for the height of the frames of the video feed, in pixels.

        @return: An int which is the height of the video feed frames in pixels.
        """
        if self.__video_capture__ is None:
            return 0
        else:
            height = self.__video_capture__.get(cv2.CAP_PROP_FRAME_HEIGHT)
            return int(height)

    def get_total_frame_count(self) -> int:
        """
        A getter for the total number of frames in the video file being analysed.  Should return a value of '0' if the
        video feed is invalid for some reason.

        @return: An int which is the total number of frames in this video feed.
        """
        if self.__video_capture__ is None:
            return 0
        else:
            return self.__video_capture__.get(cv2.CAP_PROP_FRAME_COUNT)

    def get_current_frame_number(self):
        """
        A getter for the number of the frame in the video feed which the current bounding boxes were identified in.
        Should return a value of '0' if the video feed is invalid for some reason.

        @return: An int which is the current frame number.
        """
        if self.__video_capture__ is None:
            return 0
        else:
            return self.__video_capture__.get(cv2.CAP_PROP_POS_FRAMES)

    def get_fps(self) -> float:
        """
        A getter for the framerate of the current video feed, expressed as a decimal of the number of frames per second.

        @return: A float which is the framerate in fps.
        """
        if self.__video_capture__ is None:
            return 0.0
        else:
            return self.__video_capture__.get(cv2.CAP_PROP_FPS)

    def set_detection_confidence_threshold(self, threshold: float):
        """
        A setter for the minimum confidence level required to report an object, expressed as a decimal.  A value of 0.0
        corresponds to no minimum confidence level required, and a value of 1.0 requires certainty before allowing an
        object to be reported.

        @param threshold: A float which is the minimum confidence threshold for reporting detected objects.
        @return:
        """
        self.__detection_confidence_threshold__ = threshold

    def set_nms_overlap_threshold(self, threshold: float):
        """
        A setter for the amount of overlap allowed before the Non-Maximum Suppression system suppresses a given
        detection.

        @param threshold: The amount an object can overlap another one before the NMS system suppresses it.
        @return:
        """
        self.__nms_overlap_threshold__ = threshold

    def set_nms_eta_parameter(self, eta: float | None):
        """
        A setter for the 'Eta' parameter used in the Non-Maximum Suppression system.

        @param eta: A float which is the Eta parameter for NMS.  Can be set to 'None'.
        @return:
        """
        self.__nms_eta__ = eta

    def set_nms_top_k_parameter(self, top_k: float | None):
        """
        A setter for the 'Top K' parameter used in the Non-Maximum Suppression system.  This makes the system only keep
        the top 'K' results, when listed by confidence.

        @param top_k: A float which is the Top K parameter for NMS.  Can be set to 'None'.
        @return:
        """
        self.__nms_keep_top_k_indices__ = top_k

    def set_perform_nms(self, perform_nms: bool):
        """
        A setter for the perform_nms flag.  When this is set to false, Non-Maximum Suppression is not performed on the
        results.

        @param perform_nms: A bool which states whether or not to perform NMS.
        @return:
        """
        self.__should_perform_nms__ = perform_nms

    def __perform_nms__(self, detection_results: dict) -> dict:
        """
        Performs Non-Maximum Suppression of overlapping detection results.  Takes, and returns, data in the OpenCV2
        results format.

        @param detection_results: A dict which is the detection results to perform NMS on.  Should be in CV2 format.
        @return: A dict which is the results (in CV2 format), which have had NMS performed on them.
        """
        integer_bboxes = list()
        for i in detection_results["detection_boxes"]:
            a = int(i[0] * 1000)
            b = int(i[1] * 1000)
            c = int(i[2] * 1000) - a
            d = int(i[3] * 1000) - b
            integer_bboxes.append([a, b, c, d])

        indexes = cv2.dnn.NMSBoxes(integer_bboxes, detection_results["detection_scores"],
                                   self.__detection_confidence_threshold__,
                                   self.__nms_overlap_threshold__,
                                   self.__nms_eta__,
                                   self.__nms_keep_top_k_indices__)

        indexes = list(indexes)

        new_results: dict = dict()
        new_results["detection_boxes"] = list()
        new_results["detection_scores"] = list()
        new_results["detection_class_entities"] = list()
        new_results["detection_class_names"] = list()
        new_results["detection_class_labels"] = list()

        for i in reversed(range(len(detection_results["detection_boxes"]))):
            if i == indexes[-1]:
                new_results["detection_boxes"].append(detection_results["detection_boxes"][i])
                new_results["detection_scores"].append(detection_results["detection_scores"][i])
                new_results["detection_class_entities"].append(detection_results["detection_class_entities"][i])
                new_results["detection_class_names"].append(detection_results["detection_class_names"][i])
                new_results["detection_class_labels"].append(detection_results["detection_class_labels"][i])

                del indexes[-1]
        return new_results
