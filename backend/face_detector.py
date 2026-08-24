import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = python.BaseOptions

options = vision.FaceDetectorOptions(
    base_options=BaseOptions(
        model_asset_path="../models/blaze_face_short_range.tflite"
    )
)

detector = vision.FaceDetector.create_from_options(options)


def detect_face(input_path, output_path):

    image = cv2.imread(input_path)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    detection_result = detector.detect(mp_image)

    for detection in detection_result.detections:

        bbox = detection.bounding_box

        x = bbox.origin_x
        y = bbox.origin_y
        w = bbox.width
        h = bbox.height

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

    cv2.imwrite(output_path, image)

    return output_path