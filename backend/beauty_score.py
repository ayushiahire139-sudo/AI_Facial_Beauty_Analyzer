import os
import math
import pickle
import numpy as np

def extract_facial_features(face_landmarks):
    if not face_landmarks or len(face_landmarks) == 0:
        return None
        
    landmarks = face_landmarks[0]
    
    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
        
    try:
        face_height = distance(landmarks[10], landmarks[152]) # Forehead to Chin
        face_width = distance(landmarks[234], landmarks[454])  # Cheek to Cheek
        
        jaw_width = distance(landmarks[172], landmarks[397])
        
        eye_distance = distance(landmarks[133], landmarks[362])
        left_eye_width = distance(landmarks[33], landmarks[133])
        right_eye_width = distance(landmarks[362], landmarks[263])
        avg_eye_width = (left_eye_width + right_eye_width) / 2.0
        
        nose_width = distance(landmarks[98], landmarks[327])
        nose_height = distance(landmarks[6], landmarks[1])
        
        mouth_width = distance(landmarks[61], landmarks[291])
        mouth_height = distance(landmarks[13], landmarks[14])
        
        if face_width == 0 or face_height == 0 or nose_width == 0:
            return None
            
        ratio_face_hw = face_height / face_width
        ratio_jaw_face_w = jaw_width / face_width
        ratio_eyes_face_w = eye_distance / face_width
        ratio_eye_w_face_w = avg_eye_width / face_width
        ratio_nose_w_face_w = nose_width / face_width
        ratio_nose_h_face_h = nose_height / face_height
        ratio_mouth_w_face_w = mouth_width / face_width
        ratio_mouth_h_face_h = mouth_height / face_height
        ratio_mouth_nose_w = mouth_width / nose_width
        
        return [
            ratio_face_hw,
            ratio_jaw_face_w,
            ratio_eyes_face_w,
            ratio_eye_w_face_w,
            ratio_nose_w_face_w,
            ratio_nose_h_face_h,
            ratio_mouth_w_face_w,
            ratio_mouth_h_face_h,
            ratio_mouth_nose_w
        ]
    except Exception as e:
        print("Feature extraction failed:", e)
        return None

def calculate_beauty_score(face_landmarks, symmetry_score):
    """
    Calculates the overall beauty score.
    If models/beauty_predictor.pkl exists, uses the ML model to predict.
    Otherwise, falls back to the facial symmetry calculation.
    """
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models",
        "beauty_predictor.pkl"
    )

    if os.path.exists(model_path) and face_landmarks:
        try:
            with open(model_path, "rb") as f:
                model_data = pickle.load(f)
                
            model = model_data if hasattr(model_data, "predict") else model_data.get("model")
            features = extract_facial_features(face_landmarks)
            
            if features is not None and model is not None:
                X = np.array([features])
                predicted_score = model.predict(X)[0]
                predicted_score = max(0, min(100, predicted_score))
                return round(float(predicted_score), 2)
        except Exception as e:
            print("Error running beauty ML model, falling back to symmetry:", e)

    # Rule-based fallback
    if symmetry_score < 0:
        symmetry_score = 0

    if symmetry_score > 100:
        symmetry_score = 100

    return round(symmetry_score, 2)