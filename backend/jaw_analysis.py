def analyze_jaw(face_landmarks):
    """
    Analyze jaw width and shape.
    """

    if not face_landmarks:
        return {
            "jaw_width": "Unknown",
            "jaw_shape": "Unknown"
        }

    landmarks = face_landmarks[0]

    left_jaw = landmarks[172]
    right_jaw = landmarks[397]

    jaw_width = abs(right_jaw.x - left_jaw.x)

    if jaw_width < 0.20:
        jaw_type = "Narrow"

    elif jaw_width < 0.30:
        jaw_type = "Medium"

    else:
        jaw_type = "Wide"

    return {
        "jaw_width": jaw_type,
        "jaw_shape": "Balanced"
    }