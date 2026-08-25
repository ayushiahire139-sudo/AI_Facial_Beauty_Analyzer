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
    if image is None:
        return output_path, []

    # 1. Downscale large images (e.g. 4000x2252) to max 1200px to ensure ML anchors match
    h, w = image.shape[:2]
    max_dim = 1200
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        image = cv2.resize(image, (int(w * scale), int(h * scale)))
        h, w = image.shape[:2]

    # 2. Try the 4 rotation states to find the upright face
    rotations = [
        (0, image),
        (90, cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)),
        (180, cv2.rotate(image, cv2.ROTATE_180)),
        (270, cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE))
    ]

    detected_landmarks = []
    upright_image = image

    for angle, rotated_img in rotations:
        rgb = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )
        result = landmarker.detect(mp_image)
        
        if result.face_landmarks and len(result.face_landmarks) > 0:
            detected_landmarks = result.face_landmarks
            upright_image = rotated_img
            print(f"Face landmarks successfully detected after {angle}° auto-rotation correction.")
            break

    # 3. Overwrite the original uploaded path with the corrected upright image
    # This fixes the sideways display bug on the frontend results page comparison slider!
    cv2.imwrite(input_path, upright_image)

    # 4. Generate landmarks overlay image
    landmarks_overlay = upright_image.copy()
    if detected_landmarks:
        uh, uw, _ = landmarks_overlay.shape
        for landmark in detected_landmarks[0]:
            x = int(landmark.x * uw)
            y = int(landmark.y * uh)
            cv2.circle(landmarks_overlay, (x, y), 1, (0, 255, 0), -1)

    cv2.imwrite(output_path, landmarks_overlay)
    return output_path, detected_landmarks
