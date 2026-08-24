def calculate_golden_ratio(face_landmarks):
    """
    Calculate a simple Golden Ratio score using
    face height and face width.
    """

    if not face_landmarks:
        return 0

    landmarks = face_landmarks[0]

    # Face height
    forehead = landmarks[10]
    chin = landmarks[152]
    face_height = abs(chin.y - forehead.y)

    # Face width
    left_cheek = landmarks[234]
    right_cheek = landmarks[454]
    face_width = abs(right_cheek.x - left_cheek.x)

    if face_width == 0:
        return 0

    ratio = face_height / face_width

    ideal_ratio = 1.618

    difference = abs(ratio - ideal_ratio)

    score = max(0, 100 - (difference * 100))

    return round(score, 2)