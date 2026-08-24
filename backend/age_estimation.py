def estimate_age(face_landmarks):
    """
    Estimate age group using facial landmarks.
    """

    if not face_landmarks:
        return "Unknown"

    landmarks = face_landmarks[0]

    forehead = landmarks[10]
    chin = landmarks[152]

    face_height = abs(chin.y - forehead.y)

    if face_height < 0.32:
        return "15-20 Years"

    elif face_height < 0.38:
        return "21-30 Years"

    elif face_height < 0.45:
        return "31-40 Years"

    elif face_height < 0.52:
        return "41-50 Years"

    else:
        return "50+ Years"