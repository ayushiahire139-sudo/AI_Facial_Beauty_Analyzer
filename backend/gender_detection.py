def detect_gender(face_landmarks):
    """
    Simple gender estimation using facial proportions.
    """

    if not face_landmarks:
        return "Unknown"

    landmarks = face_landmarks[0]

    face_width = abs(landmarks[234].x - landmarks[454].x)
    jaw_width = abs(landmarks[172].x - landmarks[397].x)

    ratio = jaw_width / face_width

    if ratio > 0.82:
        return "Male"
    else:
        return "Female"