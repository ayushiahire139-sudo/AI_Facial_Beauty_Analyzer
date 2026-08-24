def analyze_lips(face_landmarks):
    """
    Analyze lip width and height.
    """

    if not face_landmarks:
        return {
            "lip_width": "Unknown",
            "lip_height": "Unknown",
            "lip_shape": "Unknown"
        }

    landmarks = face_landmarks[0]

    # Lip landmarks
    left_corner = landmarks[61]
    right_corner = landmarks[291]

    upper_lip = landmarks[13]
    lower_lip = landmarks[14]

    width = abs(right_corner.x - left_corner.x)
    height = abs(lower_lip.y - upper_lip.y)

    # Width
    if width < 0.18:
        lip_width = "Small"
    elif width < 0.30:
        lip_width = "Medium"
    else:
        lip_width = "Wide"

    # Height
    if height < 0.02:
        lip_height = "Thin"
    elif height < 0.05:
        lip_height = "Medium"
    else:
        lip_height = "Full"

    return {
        "lip_width": lip_width,
        "lip_height": lip_height,
        "lip_shape": "Balanced"
    }