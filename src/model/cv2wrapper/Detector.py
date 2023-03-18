import cv2
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
from PIL import ImageColor
from PIL.Image import Image
from PIL import Image

from PIL import ImageDraw
from PIL import ImageFont

from model.cv2wrapper import BoundingBoxFactory
from util.DebugPrint import debug_print


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


class Detector:

    def __init__(self, model_url: str, file_path=0):
        self.model = hub.load(model_url).signatures['default']
        self.video_capture = cv2.VideoCapture(file_path)
        self.current_frame = None

    def try_loading_next_frame(self) -> bool:
        try:
            _, self.current_frame = self.video_capture.read()
            has_next_frame = self.current_frame is not None
        except cv2.error:
            has_next_frame = False

        return has_next_frame

    def get_frame_with_boxes(self, detection_threshold=0.5) -> (Image, list):
        image_without_boxes = self.current_frame
        detection_results = self.__get_detection_results__(image_without_boxes)
        bounding_boxes = BoundingBoxFactory.get_bounding_box_list(detection_results, detection_threshold)
        return draw_boxes(image_without_boxes,
                          detection_results["detection_boxes"],
                          detection_results["detection_class_entities"],
                          detection_results["detection_scores"]), bounding_boxes

    def __get_detection_results__(self, frame):
        converted_img = tf.image.convert_image_dtype(frame, tf.float32)[tf.newaxis, ...]
        results = self.model(converted_img)
        results = {key: value.numpy() for key, value in results.items()}
        return results

    def get_frame_width(self) -> int:
        if self.video_capture is None:
            return 0
        else:
            width = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            return int(width)

    def get_frame_height(self) -> int:
        if self.video_capture is None:
            return 0
        else:
            height = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
            return int(height)
