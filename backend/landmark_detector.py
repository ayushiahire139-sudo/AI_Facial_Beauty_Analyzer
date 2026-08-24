import cv2
import mediapipe as mp
import os

BaseOptions = mp.tasks.BaseOptions
Vision = mp.tasks.vision

FaceLandmarker = Vision.FaceLandmarker
FaceLandmarkerOptions = Vision.FaceLandmarkerOptions
RunningMode = Vision.RunningMode

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "face_landmarker.task"
)

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.IMAGE,
    num_faces=1
)

landmarker = FaceLandmarker.create_from_options(options)


def detect_landmarks(input_path, output_path):
    image = cv2.imread(input_path)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = landmarker.detect(mp_image)

    if result.face_landmarks:
        h, w, _ = image.shape

        for landmark in result.face_landmarks[0]:
            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.circle(image, (x, y), 1, (0, 255, 0), -1)

    cv2.imwrite(output_path, image)

    print(type(result.face_landmarks))
    print(len(result.face_landmarks))

    return output_path, result.face_landmarks
