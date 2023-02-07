import cv2
import mediapipe as mp

from util.ObjectRecognition.IObjectRecognition import IObjectRecognition


class MediaPipe(IObjectRecognition):
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_objectron = mp.solutions.objectron

    def go(self):

        # For static images:
        IMAGE_FILES = ["C:/Users/hughm/Desktop/Geek Stuff/Images/Banana-Single.jpg"]

        with self.mp_objectron.Objectron(static_image_mode=True,
                                         max_num_objects=5,
                                         min_detection_confidence=0.5,
                                         model_name='Banana') as objectron:
            for idx, file in enumerate(IMAGE_FILES):
                image = cv2.imread(file)
                # Convert the BGR image to RGB and process it with MediaPipe Objectron.
                results = objectron.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                # Draw box landmarks.
                if not results.detected_objects:
                    print(f'No box landmarks detected on {file}')
                    continue
                print(f'Box landmarks of {file}:')
                annotated_image = image.copy()
                for detected_object in results.detected_objects:
                    self.mp_drawing.draw_landmarks(
                        annotated_image, detected_object.landmarks_2d, self.mp_objectron.BOX_CONNECTIONS)
                    self.mp_drawing.draw_axis(annotated_image, detected_object.rotation,
                                              detected_object.translation)
                    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
