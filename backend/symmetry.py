import math

def calculate_symmetry(face_landmarks):

    if not face_landmarks:
        return 0

    landmarks = face_landmarks[0]

    # Centre of face
    center_x = landmarks[1].x

    # Correct left-right landmark pairs
    landmark_pairs = [
        (33, 263),
        (133, 362),
        (61, 291),
        (234, 454),
        (172, 397),
        (58, 288),
        (136, 365),
        (93, 323)
    ]

    total_difference = 0

    for left_index, right_index in landmark_pairs:

        left = landmarks[left_index]
        right = landmarks[right_index]

        left_distance = abs(left.x - center_x)
        right_distance = abs(right.x - center_x)

        total_difference += abs(
            left_distance - right_distance
        )

    average_difference = total_difference / len(landmark_pairs)

    print("Average Difference:", average_difference)

    symmetry_score = max(
        0,
        100 - average_difference * 300
    )

    print("Symmetry Score:", symmetry_score)

    return round(symmetry_score, 2)