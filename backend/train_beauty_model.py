# ==========================================================================
# AI FACIAL BEAUTY ANALYZER - MODEL TRAINING PIPELINE
# ==========================================================================

import os
import math
import pickle
import numpy as np
import cv2
import mediapipe as mp

# MediaPipe Initialization for Real Image Processing
BaseOptions = mp.tasks.BaseOptions
Vision = mp.tasks.vision
FaceLandmarker = Vision.FaceLandmarker
FaceLandmarkerOptions = Vision.FaceLandmarkerOptions
RunningMode = Vision.RunningMode

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "face_landmarker.task"
)

# Feature Extractor: Computes scale-invariant distance ratios
def extract_facial_features(face_landmarks):
    if not face_landmarks or len(face_landmarks) == 0:
        return None
        
    landmarks = face_landmarks[0]
    
    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
        
    try:
        # 1. Height & Width of Face
        face_height = distance(landmarks[10], landmarks[152]) # Forehead to Chin
        face_width = distance(landmarks[234], landmarks[454])  # Cheekbone to Cheekbone
        
        # 2. Jaw Width
        jaw_width = distance(landmarks[172], landmarks[397])
        
        # 3. Eyes proportions
        eye_distance = distance(landmarks[133], landmarks[362]) # Inter-ocular distance
        left_eye_width = distance(landmarks[33], landmarks[133])
        right_eye_width = distance(landmarks[362], landmarks[263])
        avg_eye_width = (left_eye_width + right_eye_width) / 2.0
        
        # 4. Nose proportions
        nose_width = distance(landmarks[98], landmarks[327])
        nose_height = distance(landmarks[6], landmarks[1])
        
        # 5. Mouth proportions
        mouth_width = distance(landmarks[61], landmarks[291])
        mouth_height = distance(landmarks[13], landmarks[14])
        
        if face_width == 0 or face_height == 0 or nose_width == 0:
            return None
            
        # Ratios
        ratio_face_hw = face_height / face_width                # Ideal: ~1.618
        ratio_jaw_face_w = jaw_width / face_width              # Ideal: ~0.75
        ratio_eyes_face_w = eye_distance / face_width           # Ideal: ~0.25
        ratio_eye_w_face_w = avg_eye_width / face_width          # Ideal: ~0.08
        ratio_nose_w_face_w = nose_width / face_width           # Ideal: ~0.10
        ratio_nose_h_face_h = nose_height / face_height         # Ideal: ~0.10
        ratio_mouth_w_face_w = mouth_width / face_width         # Ideal: ~0.25
        ratio_mouth_h_face_h = mouth_height / face_height       # Ideal: ~0.03
        ratio_mouth_nose_w = mouth_width / nose_width           # Ideal: ~2.5
        
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
        print("Error during feature extraction:", e)
        return None

# Generate Synthetic dataset matching neoclassical proportions
def generate_synthetic_data(num_samples=400):
    print(f"Generating {num_samples} synthetic face proportions mapping...")
    
    np.random.seed(42)
    X = []
    y = []
    
    for _ in range(num_samples):
        # Sample realistic ranges for ratios with normal variations
        f_hw = np.random.normal(1.618, 0.15)
        f_jaw_w = np.random.normal(0.76, 0.08)
        f_eye_d = np.random.normal(0.25, 0.04)
        f_eye_w = np.random.normal(0.08, 0.015)
        f_nose_w = np.random.normal(0.10, 0.02)
        f_nose_h = np.random.normal(0.10, 0.02)
        f_mouth_w = np.random.normal(0.25, 0.04)
        f_mouth_h = np.random.normal(0.03, 0.01)
        f_mouth_nose = np.random.normal(2.5, 0.4)
        
        features = [f_hw, f_jaw_w, f_eye_d, f_eye_w, f_nose_w, f_nose_h, f_mouth_w, f_mouth_h, f_mouth_nose]
        X.append(features)
        
        # Calculate a beauty score (0-100) based on closeness to ideal canons
        score = 100.0
        score -= abs(f_hw - 1.618) * 60            # Golden ratio face height/width
        score -= abs(f_jaw_w - 0.75) * 50          # Balanced jaw line
        score -= abs(f_eye_d - 0.25) * 50          # Inter-ocular distance
        score -= abs(f_nose_w - 0.10) * 100        # Balanced nose width
        score -= abs(f_mouth_w - 0.25) * 60        # Balanced mouth width
        score -= abs(f_mouth_nose - 2.5) * 30      # Mouth-to-nose ratio
        
        # Add random human rating variance
        score += np.random.normal(0, 4)
        score = max(40.0, min(100.0, score))
        
        y.append(score)
        
    return np.array(X), np.array(y)

# Extract landmarks and labels from real dataset folder
def load_real_dataset(csv_path, images_dir):
    print(f"Loading real dataset from {csv_path}...")
    import pandas as pd
    
    df = pd.read_csv(csv_path)
    
    # Setup landmarker
    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=RunningMode.IMAGE,
        num_faces=1
    )
    landmarker = FaceLandmarker.create_from_options(options)
    
    X = []
    y = []
    
    for idx, row in df.iterrows():
        img_name = row['filename']
        rating = row['rating'] # score between 0 and 100
        
        img_path = os.path.join(images_dir, img_name)
        if not os.path.exists(img_path):
            print(f"Skipping: {img_name} (File not found at {img_path})")
            continue
            
        image = cv2.imread(img_path)
        if image is None:
            continue
            
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        result = landmarker.detect(mp_image)
        if result.face_landmarks:
            features = extract_facial_features(result.face_landmarks)
            if features is not None:
                X.append(features)
                y.append(rating)
                
    landmarker.close()
    return np.array(X), np.array(y)

def train_pipeline():
    # Attempt to load Scikit-Learn
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_absolute_error, r2_score
    except ImportError:
        print("Scikit-Learn not found. Installing now...")
        import subprocess
        subprocess.check_call(["pip", "install", "scikit-learn", "pandas"])
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_absolute_error, r2_score

    # Paths Setup
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(project_dir, "dataset")
    csv_path = os.path.join(dataset_dir, "ratings.csv")
    models_dir = os.path.join(project_dir, "models")
    model_output_path = os.path.join(models_dir, "beauty_predictor.pkl")
    
    # Check if a real dataset is provided
    if os.path.exists(csv_path) and len(os.listdir(dataset_dir)) > 1:
        print("Found real dataset (ratings.csv). Running training on custom images...")
        X, y = load_real_dataset(csv_path, dataset_dir)
        if len(X) < 10:
            print("Dataset too small (<10 samples). Bootstrapping with synthetic data...")
            X_syn, y_syn = generate_synthetic_data()
            if len(X) > 0:
                X = np.vstack((X_syn, X))
                y = np.concatenate((y_syn, y))
            else:
                X, y = X_syn, y_syn
    else:
        print("No ratings.csv or image files found in dataset folder.")
        X, y = generate_synthetic_data()
        
    print(f"Total dataset size: {len(X)} samples.")
    
    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Regressor model
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print("\n--- Model Training Results ---")
    print(f"Mean Absolute Error (MAE): {mae:.3f} points")
    print(f"R-squared Score (R2): {r2:.3f}")
    print("------------------------------\n")
    
    # Save the model
    os.makedirs(models_dir, exist_ok=True)
    with open(model_output_path, "wb") as f:
        pickle.dump({"model": model, "feature_names": [
            "ratio_face_hw", "ratio_jaw_face_w", "ratio_eyes_face_w",
            "ratio_eye_w_face_w", "ratio_nose_w_face_w", "ratio_nose_h_face_h",
            "ratio_mouth_w_face_w", "ratio_mouth_h_face_h", "ratio_mouth_nose_w"
        ]}, f)
        
    print(f"Success! Beauty prediction model saved to {model_output_path}")
    print("\nTo train on real ratings, place face photos in 'dataset/' folder and create a 'ratings.csv'")
    print("with columns 'filename' and 'rating' (e.g. filename=face1.jpg, rating=82.5), then run this script again.")

if __name__ == "__main__":
    train_pipeline()
