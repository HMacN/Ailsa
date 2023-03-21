from time import sleep

import cv2
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
from PIL import ImageColor
from PIL.Image import Image
from PIL import Image

from PIL import ImageDraw
from PIL import ImageFont

from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box
from util.Debugging import debug_print


def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())

    font = ImageFont.load_default()

    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            y_min, x_min, y_max, x_max = tuple(boxes[i])
            display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                           int(100 * scores[i]))
            color = colors[hash(class_names[i]) % len(colors)]
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box_on_image(image_pil, y_min, x_min, y_max, x_max, color, font,
                                       display_str_list=[display_str])
            np.copyto(image, np.array(image_pil))
    return image


def draw_bounding_box_on_image(image,
                               y_min,
                               x_min,
                               y_max,
                               x_max,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (x_min * im_width, x_max * im_width,
                                  y_min * im_height, y_max * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
               (left, top)],
              width=thickness,
              fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getbbox(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        box = font.getbbox(display_str)
        text_width = box[2]
        text_height = box[3]
        margin = np.ceil(0.05 * text_height)
        t1: float = left
        t2: float = text_bottom - text_height - 2 * margin
        t3: float = left + text_width
        t4: float = text_bottom
        draw.rectangle((t1, t2, t3, t4),
                       fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                  display_str,
                  fill="black",
                  font=font)
        text_bottom -= text_height - 2 * margin


def print_tf_state():
    # Print Tensorflow version
    print(tf.__version__)

    # Check available GPU devices.
    print("The following GPU devices are available: %s" % tf.test.gpu_device_name())


def __convert_cv2_results_to_bounding_box_collection__(detection_results) -> BoundingBoxCollection:
    number_of_boxes = len(detection_results["detection_boxes"])
    boxes = BoundingBoxCollection()

    for i in range(number_of_boxes):
        new_box = Box(left_edge=detection_results["detection_boxes"][i][1],
                      right_edge=detection_results["detection_boxes"][i][0],
                      lower_edge=detection_results["detection_boxes"][i][2],
                      upper_edge=detection_results["detection_boxes"][i][3],
                      confidence=detection_results["detection_scores"][i],
                      label=detection_results["detection_class_entities"][i])
        boxes.add(new_box)

    return boxes


class Detector:

    def __init__(self, model_url: str, file_path=0):
        self.__model__ = hub.load(model_url).signatures['default']
        self.__video_capture__ = cv2.VideoCapture(file_path)
        self.__current_frame__ = None
        self.__current_frame_with_bounding_boxes__ = None
        self.__current_bounding_boxes__ = None

    def try_loading_next_frame(self) -> bool:
        try:
            _, self.__current_frame__ = self.__video_capture__.read()
            has_next_frame = self.__current_frame__ is not None
        except cv2.error:
            has_next_frame = False

        return has_next_frame

    def run_detection_on_current_frame(self, detection_threshold=0.5):
        detection_results = self.__get_detection_results__()
        bounding_boxes = __convert_cv2_results_to_bounding_box_collection__(detection_results)
        bounding_boxes.trim_by_confidence(detection_threshold)
        self.__current_bounding_boxes__ = bounding_boxes
        self.__current_frame_with_bounding_boxes__ = draw_boxes(self.__current_frame__,
                                                                detection_results["detection_boxes"],
                                                                detection_results["detection_class_entities"],
                                                                detection_results["detection_scores"],
                                                                min_score=detection_threshold)

    def get_frame_without_bounding_boxes(self) -> Image:
        return self.__current_frame__

    def get_frame_with_bounding_boxes(self) -> Image:
        return self.__current_frame_with_bounding_boxes__

    def get_bounding_boxes(self) -> BoundingBoxCollection:
        return self.__current_bounding_boxes__

    def __get_detection_results__(self):
        converted_img = tf.image.convert_image_dtype(self.__current_frame__, tf.float32)[tf.newaxis, ...]
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
