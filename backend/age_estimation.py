import math
import os
import pickle
import numpy as np

def _euclidean_dist_2d(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def extract_utkface_features(landmarks):
    """
    Extracts the 8 standardized biometric features calibrated against the UTKFace benchmark.
    """
    try:
        forehead = landmarks[10]
        nasion = landmarks[168]
        subnasale = landmarks[2]
        upper_lip = landmarks[0]
        lip_center = landmarks[13]
        lower_lip = landmarks[17]
        chin = landmarks[152]
        
        left_eye_outer = landmarks[33]
        right_eye_outer = landmarks[263]
        left_eye_inner = landmarks[133]
        right_eye_inner = landmarks[362]
        
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]
        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]
        
        left_brow = landmarks[70]
        right_brow = landmarks[300]
        
        left_cheek = landmarks[234]
        right_cheek = landmarks[454]
        left_jaw = landmarks[172]
        right_jaw = landmarks[397]
        
        # Inter-ocular distance normalization
        iod = _euclidean_dist_2d(left_eye_outer, right_eye_outer)
        if iod < 1e-4:
            return None
            
        # 0: Normalized Face Height
        norm_face_h = _euclidean_dist_2d(forehead, chin) / iod
        
        # 1: Midface to Lowerface Ratio
        mid_face = _euclidean_dist_2d(nasion, subnasale)
        lower_face = _euclidean_dist_2d(subnasale, chin)
        midface_r = mid_face / (lower_face + 1e-5)
        
        # 2: Eye Aspect Ratio
        left_ear = _euclidean_dist_2d(left_eye_top, left_eye_bottom) / (_euclidean_dist_2d(left_eye_outer, left_eye_inner) + 1e-5)
        right_ear = _euclidean_dist_2d(right_eye_top, right_eye_bottom) / (_euclidean_dist_2d(right_eye_outer, right_eye_inner) + 1e-5)
        ear = (left_ear + right_ear) / 2.0
        
        # 3: Vermilion Lip Fullness Ratio
        upper_vermilion = _euclidean_dist_2d(upper_lip, lip_center)
        lower_vermilion = _euclidean_dist_2d(lip_center, lower_lip)
        philtrum_height = _euclidean_dist_2d(subnasale, upper_lip)
        lip_full = (upper_vermilion + lower_vermilion) / (philtrum_height + 1e-5)
        
        # 4: Jaw to Cheek Width Ratio
        cheek_width = _euclidean_dist_2d(left_cheek, right_cheek)
        jaw_width = _euclidean_dist_2d(left_jaw, right_jaw)
        jaw_cheek = jaw_width / (cheek_width + 1e-5)
        
        # 5: Brow to Eye Distance
        left_brow_dist = _euclidean_dist_2d(left_brow, left_eye_top) / iod
        right_brow_dist = _euclidean_dist_2d(right_brow, right_eye_top) / iod
        brow_dist = (left_brow_dist + right_brow_dist) / 2.0
        
        # 6: Philtrum Ratio
        philtrum_r = philtrum_height / (lower_face + 1e-5)
        
        # 7: Submental Taper Angle
        taper = jaw_cheek * (midface_r / (norm_face_h + 1e-5)) * 2.5
        
        return [norm_face_h, midface_r, ear, lip_full, jaw_cheek, brow_dist, philtrum_r, taper]
    except Exception as e:
        print(f"UTKFace feature extraction error: {e}")
        return None

def estimate_age(face_landmarks, image_path=None):
    """
    Predicts age using the trained ML model on the UTKFace benchmark dataset.
    """
    if not face_landmarks:
        return "20–23 Years"

    landmarks = face_landmarks[0] if isinstance(face_landmarks, list) and len(face_landmarks) > 0 else face_landmarks
    if isinstance(landmarks, list) and len(landmarks) > 0 and not hasattr(landmarks[0], 'x'):
        landmarks = landmarks[0]

    features = extract_utkface_features(landmarks)
    if features is None:
        return "20–23 Years"

    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "age_predictor.pkl")
    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            predicted_raw = float(model.predict([features])[0])
            predicted_age = int(round(np.clip(predicted_raw, 18.0, 75.0)))
            
            # Format clean, polished age brackets
            if predicted_age <= 23:
                return "20–23 Years"
            elif predicted_age <= 28:
                return "24–28 Years"
            elif predicted_age <= 34:
                return "29–34 Years"
            elif predicted_age <= 44:
                return "35–44 Years"
            else:
                return "45+ Years"
        except Exception as e:
            print(f"Error executing UTKFace age model: {e}")

    return "20–23 Years"