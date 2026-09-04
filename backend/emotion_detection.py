import math

def _euclidean_dist_2d(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def detect_emotion(face_landmarks):
    """
    Advanced Emotion Detection based on Paul Ekman's Facial Action Coding System (FACS).
    Evaluates Action Units (AUs):
    - AU6 + AU12: Zygomatic major & orbicularis oculi (Duchenne Smile - Joy/Happy)
    - AU4: Corrugator supercilii (Brow furrowing - Focused/Intense)
    - AU1 + AU2 + AU26: Frontalis & jaw drop (Eyebrow raise & mouth opening - Surprised)
    - AU15: Depressor anguli oris (Mouth corner depression - Thoughtful/Pensive)
    - AU0: Baseline balanced resting muscle tone (Serene / Calm / Composed)
    """
    if not face_landmarks:
        return "Calm & Serene"

    landmarks = face_landmarks[0] if isinstance(face_landmarks, list) and len(face_landmarks) > 0 else face_landmarks
    if isinstance(landmarks, list) and len(landmarks) > 0 and not hasattr(landmarks[0], 'x'):
        landmarks = landmarks[0]

    try:
        # Mouth Corner & Lip Landmarks
        mouth_left = landmarks[61]
        mouth_right = landmarks[291]
        upper_lip = landmarks[0]
        upper_lip_inner = landmarks[13]
        lower_lip_inner = landmarks[14]
        lower_lip = landmarks[17]
        
        # Eyes & Brow Landmarks
        left_brow_inner = landmarks[70]
        right_brow_inner = landmarks[300]
        left_brow_mid = landmarks[105]
        right_brow_mid = landmarks[334]
        
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]
        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]
        
        left_eye_outer = landmarks[33]
        right_eye_outer = landmarks[263]
        
        # Inter-ocular normalization
        iod = _euclidean_dist_2d(left_eye_outer, right_eye_outer)
        if iod < 1e-4:
            return "Calm & Serene"

        # 1. Smile & Zygomatic Action (AU12)
        mouth_width = _euclidean_dist_2d(mouth_left, mouth_right)
        mouth_width_norm = mouth_width / iod  # Baseline neutral ~ 0.70 - 0.80, Smile > 0.88
        
        # Mouth Corner Elevation relative to lip center
        mouth_corners_y = (mouth_left.y + mouth_right.y) / 2.0
        lip_center_y = (upper_lip_inner.y + lower_lip_inner.y) / 2.0
        corner_elevation = (lip_center_y - mouth_corners_y) / iod  # Positive = corners raised up (smile)
        
        # 2. Mouth Opening (AU26 / AU27)
        mouth_opening = _euclidean_dist_2d(upper_lip_inner, lower_lip_inner) / iod
        
        # 3. Brow Elevation & Arch (AU1 + AU2)
        left_brow_raise = _euclidean_dist_2d(left_brow_mid, left_eye_top) / iod
        right_brow_raise = _euclidean_dist_2d(right_brow_mid, right_eye_top) / iod
        avg_brow_raise = (left_brow_raise + right_brow_raise) / 2.0  # High > 0.22, Low < 0.14
        
        # 4. Brow Furrow (AU4 - Inter-brow distance)
        inter_brow_dist = _euclidean_dist_2d(left_brow_inner, right_brow_inner) / iod  # Narrow < 0.28 = furrowed
        
        # 5. Eye Squint / Lower Eyelid Elevation (AU6 - Duchenne smiling marker)
        left_eye_aperture = _euclidean_dist_2d(left_eye_top, left_eye_bottom) / iod
        right_eye_aperture = _euclidean_dist_2d(right_eye_top, right_eye_bottom) / iod
        avg_eye_aperture = (left_eye_aperture + right_eye_aperture) / 2.0
        
        # ----------------------------------------------------
        # FACS Classification Decision Engine
        # ----------------------------------------------------
        
        # 1. Radiant Joyful Smile (AU12 + AU6 or wide smile ratio)
        if mouth_width_norm > 0.86 or (corner_elevation > 0.018 and mouth_width_norm > 0.78):
            if mouth_opening > 0.08:
                return "Happy (Radiant Smile)"
            else:
                return "Happy (Warm Gentle Smile)"
                
        # 2. Surprised / Excited (High brows + open mouth)
        if avg_brow_raise > 0.22 and mouth_opening > 0.08:
            return "Surprised & Excited"
            
        # 3. Focused & Confident (Empowered / Executive gaze)
        if inter_brow_dist < 0.29 and avg_eye_aperture < 0.16:
            return "Focused & Confident"
            
        # 4. Thoughtful / Pensive (Reflective / subtle brow raise or downturn)
        if corner_elevation < -0.015:
            return "Thoughtful & Pensive"
            
        # 5. Pleasant / Positive Neutral
        if corner_elevation > 0.005:
            return "Pleasant & Confident"
            
        # 6. Default: Calm & Serene (Classic relaxed aesthetic)
        return "Calm & Serene"

    except Exception as e:
        print(f"Emotion detection fallback due to: {e}")
        return "Calm & Serene"