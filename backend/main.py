from recommendation_engine import generate_recommendations
from beauty_report import generate_beauty_report
from report_generator import generate_pdf_report
from emotion_detection import detect_emotion
from gender_detection import detect_gender
from age_estimation import estimate_age
from skin_tone import detect_skin_tone
from jaw_analysis import analyze_jaw
from lip_analysis import analyze_lips
from nose_analysis import analyze_nose
from eye_analysis import analyze_eyes
from golden_ratio import calculate_golden_ratio
from face_shape import detect_face_shape
from beauty_score import calculate_beauty_score
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os

import models
import schemas

from database import engine, get_db
from security import hash_password, verify_password

from face_detector import detect_face
from landmark_detector import detect_landmarks
from symmetry import calculate_symmetry

# --------------------------------------------------
# Create Database Tables
# --------------------------------------------------
models.Base.metadata.create_all(bind=engine)

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI(
    title="AI Facial Beauty Analyzer",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins (development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Home API
# --------------------------------------------------
@app.get("/")
def home():
    return {
        "success": True,
        "message": "AI Facial Beauty Analyzer Backend Running Successfully"
    }


# --------------------------------------------------
# Register API
# --------------------------------------------------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        return {
            "success": False,
            "message": "Email already registered"
        }

    hashed_password = hash_password(user.password)

    new_user = models.User(
        fullname=user.fullname,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "User Registered Successfully",
        "user_id": new_user.id
    }


# --------------------------------------------------
# Login API
# --------------------------------------------------
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if db_user is None:
        return {
            "success": False,
            "message": "User not found"
        }

    if not verify_password(user.password, db_user.password):
        return {
            "success": False,
            "message": "Invalid Password"
        }

    return {
        "success": True,
        "message": "Login Successful",
        "user_id": db_user.id,
        "fullname": db_user.fullname,
        "email": db_user.email
    }


# --------------------------------------------------
# Upload Image API
# --------------------------------------------------
@app.post("/upload-image")
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads"
    )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_image = models.UploadedImage(
        filename=file.filename,
        filepath=file_path
    )

    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return {
        "success": True,
        "message": "Image Uploaded Successfully",
        "image_id": new_image.id,
        "filename": new_image.filename,
        "filepath": new_image.filepath
    }


# --------------------------------------------------
# Face Detection API
# --------------------------------------------------
@app.post("/detect-face")
def detect_face_api(file: UploadFile = File(...)):

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads"
    )

    processed_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "processed_images"
    )

    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)

    input_path = os.path.join(upload_folder, file.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = os.path.join(
        processed_folder,
        "face_" + file.filename
    )

    detect_face(input_path, output_path)

    return {
        "success": True,
        "message": "Face Detection Completed Successfully",
        "processed_image": output_path
    }
# --------------------------------------------------
# Face Landmark API
# --------------------------------------------------
@app.post("/detect-landmarks")
def detect_landmarks_api(file: UploadFile = File(...)):

    # Upload folder
    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads"
    )

    # Processed images folder
    processed_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "processed_images"
    )

    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)

    # Save uploaded image
    input_path = os.path.join(upload_folder, file.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Output image
    output_path = os.path.join(
        processed_folder,
        "landmarks_" + file.filename
    )

    # Detect landmarks
    processed_image, landmarks = detect_landmarks(
        input_path,
        output_path
    )

    # ----------------------------
    # Face Analysis
    # ----------------------------
    symmetry_score = calculate_symmetry(landmarks)
    beauty_score = calculate_beauty_score(symmetry_score)
    face_shape = detect_face_shape(landmarks)
    golden_ratio_score = calculate_golden_ratio(landmarks)

    eye_analysis = analyze_eyes(landmarks)
    nose_analysis = analyze_nose(landmarks)
    lip_analysis = analyze_lips(landmarks)
    jaw_analysis = analyze_jaw(landmarks)

    skin_tone = detect_skin_tone(input_path)
    estimated_age = estimate_age(landmarks)
    gender = detect_gender(landmarks)
    emotion = detect_emotion(landmarks)

    # ----------------------------
    # Beauty Report
    # ----------------------------
    beauty_report = generate_beauty_report(
        beauty_score,
        symmetry_score,
        face_shape,
        golden_ratio_score,
        eye_analysis,
        nose_analysis,
        lip_analysis,
        jaw_analysis,
        skin_tone,
        estimated_age,
        gender,
        emotion
    )

    # ----------------------------
    # AI Recommendations
    # ----------------------------
    recommendations = generate_recommendations(
        beauty_score,
        face_shape,
        eye_analysis,
        nose_analysis,
        lip_analysis,
        jaw_analysis,
        skin_tone,
        emotion
    )

    # Add recommendations to beauty report
    beauty_report["recommendations"] = recommendations

    print("\n========== BEAUTY REPORT ==========")
    print(beauty_report)
    print("===================================\n")

    # ----------------------------
    # Generate PDF Report
    # ----------------------------
    pdf_path = generate_pdf_report(
        beauty_report,
        "beauty_report.pdf"
    )

    # ----------------------------
    # Return Response
    # ----------------------------
    return {
        "success": True,
        "message": "Face Analysis Completed Successfully",

        "processed_image": processed_image,

        "symmetry_score": symmetry_score,
        "beauty_score": beauty_score,

        "face_shape": face_shape,
        "golden_ratio_score": golden_ratio_score,

        "eye_analysis": eye_analysis,
        "nose_analysis": nose_analysis,
        "lip_analysis": lip_analysis,
        "jaw_analysis": jaw_analysis,

        "skin_tone": skin_tone,
        "estimated_age": estimated_age,
        "gender": gender,
        "emotion": emotion,

        "beauty_report": beauty_report,

        "pdf_report": pdf_path
    }