import cv2
import numpy as np


def detect_skin_tone(image_path):
    """
    Detect average skin tone from the image.
    """

    image = cv2.imread(image_path)

    if image is None:
        return "Unknown"

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    h, w, _ = image.shape

    # Take the center region of the image
    roi = image[h//3:2*h//3, w//3:2*w//3]

    average = np.mean(roi, axis=(0, 1))

    brightness = np.mean(average)

    if brightness > 180:
        return "Fair"

    elif brightness > 140:
        return "Light"

    elif brightness > 100:
        return "Medium"

    elif brightness > 70:
        return "Brown"

    else:
        return "Dark"