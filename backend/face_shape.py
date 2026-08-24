def detect_face_shape(face_landmarks):
    """
    Detect face shape using facial proportions.
    Returns one of:
    Oval
    Round
    Square
    Heart
    Diamond
    """

    if not face_landmarks:
        return "Face Not Detected"

    landmarks = face_landmarks[0]

    # Approximate landmark indices
    forehead = landmarks[10]
    chin = landmarks[152]

    left_cheek = landmarks[234]
    right_cheek = landmarks[454]

    left_jaw = landmarks[172]
    right_jaw = landmarks[397]

    # Measurements
    face_height = abs(chin.y - forehead.y)

    cheek_width = abs(right_cheek.x - left_cheek.x)

    jaw_width = abs(right_jaw.x - left_jaw.x)

    ratio = face_height / cheek_width

    # Simple classification
    if ratio > 1.55:
        return "Oval"

    elif jaw_width > cheek_width * 0.95:
        return "Square"

    elif ratio < 1.30:
        return "Round"

    elif cheek_width > jaw_width:
        return "Heart"

    else:
        return "Diamond"