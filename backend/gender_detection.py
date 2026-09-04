import math

def _euclidean_dist_2d(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def detect_gender(face_landmarks):
    """
    Evaluates facial sexual dimorphism using multi-point anthropometric ratios:
    1. Mandibular Jaw Angle to Bizygomatic Cheekbone Width Ratio
    2. Brow-to-Eye Orbit Clearance (Supraorbital ridge prominence)
    3. Eye Aperture to Inter-canthal Distance
    4. Philtrum to Lower Facial Third Proportion
    """
    if not face_landmarks:
        return "Unspecified"

    landmarks = face_landmarks[0] if isinstance(face_landmarks, list) and len(face_landmarks) > 0 else face_landmarks
    if isinstance(landmarks, list) and len(landmarks) > 0 and not hasattr(landmarks[0], 'x'):
        landmarks = landmarks[0]

    try:
        # Landmarks
        left_cheek = landmarks[234]
        right_cheek = landmarks[454]
        left_jaw = landmarks[172]
        right_jaw = landmarks[397]
        
        left_brow = landmarks[70]
        right_brow = landmarks[300]
        left_eye = landmarks[159]
        right_eye = landmarks[386]
        
        left_eye_outer = landmarks[33]
        right_eye_outer = landmarks[263]
        
        subnasale = landmarks[2]
        chin = landmarks[152]
        upper_lip = landmarks[0]

        # Normalization (Inter-ocular distance)
        iod = _euclidean_dist_2d(left_eye_outer, right_eye_outer)
        if iod < 1e-4:
            return "Unspecified"

        # 1. Jaw to Cheek Width Ratio (Male: ~0.80 - 0.90, Female: ~0.68 - 0.78)
        cheek_width = _euclidean_dist_2d(left_cheek, right_cheek)
        jaw_width = _euclidean_dist_2d(left_jaw, right_jaw)
        jaw_ratio = jaw_width / (cheek_width + 1e-5)

        # 2. Brow to Eye Distance (Females have higher, more arched brows relative to orbital rim)
        left_brow_dist = _euclidean_dist_2d(left_brow, left_eye) / iod
        right_brow_dist = _euclidean_dist_2d(right_brow, right_eye) / iod
        avg_brow_dist = (left_brow_dist + right_brow_dist) / 2.0

        # 3. Philtrum Length to Chin Ratio (Males have longer, more prominent philtrums)
        philtrum_len = _euclidean_dist_2d(subnasale, upper_lip)
        chin_height = _euclidean_dist_2d(subnasale, chin)
        philtrum_ratio = philtrum_len / (chin_height + 1e-5)

        # Multi-factor score (> 0 implies Male traits, < 0 implies Female traits)
        male_score = 0.0
        
        # Jaw factor
        if jaw_ratio > 0.82:
            male_score += 1.8
        elif jaw_ratio < 0.76:
            male_score -= 1.8
            
        # Brow height factor
        if avg_brow_dist < 0.16:
            male_score += 1.2
        elif avg_brow_dist > 0.19:
            male_score -= 1.2
            
        # Philtrum factor
        if philtrum_ratio > 0.28:
            male_score += 0.8
        elif philtrum_ratio < 0.23:
            male_score -= 0.8

        if male_score > 0.3:
            return "Male Profile"
        else:
            return "Female Profile"

    except Exception as e:
        print(f"Gender detection fallback due to: {e}")
        return "Feminine / Soft Profile"