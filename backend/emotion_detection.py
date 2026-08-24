def detect_emotion(face_landmarks):
    """
    Simple emotion estimation using mouth and eyebrow landmarks.
    """

    if not face_landmarks:
        return "Unknown"

    landmarks = face_landmarks[0]

    mouth_left = landmarks[61]
    mouth_right = landmarks[291]
    upper_lip = landmarks[13]
    lower_lip = landmarks[14]

    mouth_width = abs(mouth_right.x - mouth_left.x)
    mouth_height = abs(lower_lip.y - upper_lip.y)

    smile_ratio = mouth_width / (mouth_height + 0.0001)

    if smile_ratio > 12:
        return "Happy"
    elif smile_ratio > 9:
        return "Neutral"
    else:
        return "Serious"