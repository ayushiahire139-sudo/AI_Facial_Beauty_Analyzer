def analyze_nose(face_landmarks):
    """
    Analyze nose width and length.
    """

    if not face_landmarks:
        return {
            "nose_width": "Unknown",
            "nose_length": "Unknown",
            "nose_shape": "Unknown"
        }

    landmarks = face_landmarks[0]

    # Nose landmarks
    nose_tip = landmarks[1]
    nose_top = landmarks[6]
    left_nostril = landmarks[98]
    right_nostril = landmarks[327]

    # Measurements
    width = abs(right_nostril.x - left_nostril.x)
    length = abs(nose_tip.y - nose_top.y)

    # Width classification
    if width < 0.08:
        nose_width = "Narrow"
    elif width < 0.12:
        nose_width = "Medium"
    else:
        nose_width = "Wide"

    # Length classification
    if length < 0.08:
        nose_length = "Short"
    elif length < 0.13:
        nose_length = "Medium"
    else:
        nose_length = "Long"

    return {
        "nose_width": nose_width,
        "nose_length": nose_length,
        "nose_shape": "Balanced"
    }