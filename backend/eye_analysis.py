def analyze_eyes(face_landmarks):

    if not face_landmarks:
        return {
            "eye_distance": "Unknown",
            "eye_size": "Unknown",
            "eye_symmetry": "Unknown"
        }

    landmarks = face_landmarks[0]

    left_eye = landmarks[33]
    right_eye = landmarks[263]

    distance = abs(right_eye.x - left_eye.x)

    if distance > 0.30:
        eye_distance = "Wide"

    elif distance > 0.22:
        eye_distance = "Normal"

    else:
        eye_distance = "Close"

    return {
        "eye_distance": eye_distance,
        "eye_size": "Medium",
        "eye_symmetry": "Balanced"
    }