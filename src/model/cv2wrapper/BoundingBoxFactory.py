from util.BoundingBox import BoundingBox
from util.DebugPrint import debug_print


def get_bounding_box_list(detection_results, detection_threshold) -> list:
    bounding_boxes = list()

    for i in range(len(detection_results["detection_scores"])):
        confidence = detection_results["detection_scores"][i]
        if confidence > detection_threshold:

            box_height = detection_results["detection_boxes"][i][0]
            box_width = detection_results["detection_boxes"][i][1]
            box_vert_to_origin = detection_results["detection_boxes"][i][0]
            box_horiz_to_origin = detection_results["detection_boxes"][i][1]

            new_box = BoundingBox(
                box_horiz_to_origin,
                box_vert_to_origin,
                box_width,
                box_height,
                detection_results["detection_class_entities"][i])

            bounding_boxes.append(new_box)

    return bounding_boxes
