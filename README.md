# AI Facial Beauty Analyzer

An AI-powered facial analysis web application that uses computer vision and facial landmark analysis to evaluate facial features, calculate analysis scores, and generate a detailed beauty analysis report.

The project combines Python, FastAPI, MediaPipe, OpenCV, SQLAlchemy, SQLite, HTML, CSS, and JavaScript to provide an end-to-end facial analysis workflow.

## Overview

AI Facial Beauty Analyzer allows users to upload a facial image through a web interface and receive automated facial analysis.

The system performs face detection, facial landmark detection, facial feature analysis, symmetry and golden-ratio calculations, skin-tone and emotion analysis, beauty-score calculation, and report generation.

This project demonstrates how computer vision, image processing, backend APIs, databases, and frontend technologies can be combined to build a complete AI-powered application.

## Key Features

- Face detection
- Facial landmark detection
- Facial feature analysis
- Eye analysis
- Lip analysis
- Nose analysis
- Jaw analysis
- Face-shape detection
- Skin-tone analysis
- Facial symmetry analysis
- Golden-ratio analysis
- Emotion detection
- Beauty-score calculation
- Automated beauty analysis report
- User registration and login
- Password hashing
- REST API using FastAPI
- SQLite database integration
- Web-based frontend

## How It Works

```text
User
  |
  v
Web Interface
  |
  v
Image Upload
  |
  v
FastAPI Backend
  |
  +----------------------+
  |                      |
  v                      v
Face Detection      Facial Landmarks
  |                      |
  +----------+-----------+
             |
             v
     Facial Analysis
             |
     +-------+--------+----------------+
     |       |        |        |       |
     v       v        v        v       v
   Eyes    Lips     Nose     Jaw    Face Shape
     |       |        |        |       |
     +-------+--------+--------+-------+
             |
             v
   Symmetry / Golden Ratio
             |
             v
      Beauty Score
             |
             v
      Analysis Report
             |
             v
        Web Results

System Architecture:

+--------------------------------------------------+
|                  Frontend Layer                  |
|          HTML + CSS + JavaScript                 |
+-------------------------+------------------------+
                          |
                          | HTTP / REST API
                          v
+--------------------------------------------------+
|                   API Layer                      |
|                    FastAPI                      |
|                     main.py                     |
+-------------------------+------------------------+
                          |
          +---------------+----------------+
          |                                |
          v                                v
+----------------------+       +----------------------+
|  Analysis Modules    |       |   Database Layer     |
|----------------------|       |----------------------|
| Face Detection       |       | SQLAlchemy           |
| Landmarks            |       | SQLite               |
| Eyes                 |       | User Data            |
| Lips                 |       | Application Data     |
| Nose                 |       +----------------------+
| Jaw                  |
| Face Shape           |
| Skin Tone            |
| Symmetry             |
| Golden Ratio         |
| Emotion              |
| Beauty Score         |
+----------------------+
          |
          v
+----------------------+
| Report Generation    |
+----------------------+

Tech Stack
AI and Computer Vision
Python
OpenCV
MediaPipe
NumPy
Pandas
TensorFlow Lite model files
Backend
FastAPI
SQLAlchemy
SQLite
Pydantic
Password hashing
REST API
Frontend
HTML5
CSS3
JavaScript
Development Tools
Git
GitHub
GitHub CLI
Visual Studio Code
Project Structure
AI_Facial_Beauty_Analyzer/
|
+-- backend/
|   +-- main.py
|   +-- database.py
|   +-- models.py
|   +-- schemas.py
|   +-- security.py
|   +-- face_detector.py
|   +-- landmark_detector.py
|   +-- beauty_score.py
|   +-- beauty_report.py
|   +-- emotion_detection.py
|   +-- eye_analysis.py
|   +-- face_shape.py
|   +-- gender_detection.py
|   +-- golden_ratio.py
|   +-- jaw_analysis.py
|   +-- lip_analysis.py
|   +-- nose_analysis.py
|   +-- skin_tone.py
|   +-- symmetry.py
|   +-- recommendation_engine.py
|   +-- report_generator.py
|   +-- requirements.txt
|
+-- frontend/
|   +-- index.html
|   +-- home.html
|   +-- login.html
|   +-- register.html
|   +-- result.html
|   +-- CSS/
|   +-- JS/
|
+-- models/
|   +-- blaze_face_short_range.tflite
|   +-- face_landmarker.task
|
+-- docs/
+-- screenshots/
+-- requirements.txt
+-- .gitignore
+-- README.md
Installation
1. Clone the Repository
git clone https://github.com/ayushiahire139-sudo/AI_Facial_Beauty_Analyzer.git
cd AI_Facial_Beauty_Analyzer
2. Create a Virtual Environment

Windows:

python -m venv venv

Activate the virtual environment:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt

If backend dependencies are maintained separately:

pip install -r backend\requirements.txt
Backend Setup

The backend uses FastAPI and provides REST API endpoints for authentication, image processing, facial analysis, and report generation.

Move into the backend directory:

cd backend

Start the FastAPI server:

uvicorn main:app --reload

The backend will normally be available at:

http://127.0.0.1:8000
API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

http://127.0.0.1:8000/docs

OpenAPI specification:

http://127.0.0.1:8000/openapi.json

The API provides functionality related to:

User registration
User login
Image processing
Facial analysis
Beauty score calculation
Report generation
Frontend Setup

The frontend is developed using HTML, CSS, and JavaScript.

Frontend pages include:

Home page
Registration page
Login page
Image upload page
Facial analysis result page

The frontend communicates with the FastAPI backend through HTTP requests.

For local development, open the frontend using a local development server and make sure the backend is running.

Example Workflow
1. Open the web application
        |
        v
2. Register a user account
        |
        v
3. Login
        |
        v
4. Upload a facial image
        |
        v
5. FastAPI receives the image
        |
        v
6. Face detection
        |
        v
7. Facial landmark detection
        |
        v
8. Facial feature analysis
        |
        v
9. Symmetry and golden-ratio analysis
        |
        v
10. Emotion and skin-tone analysis
        |
        v
11. Beauty score calculation
        |
        v
12. Report generation
        |
        v
13. Results displayed to the user
Screenshots

Screenshots will be added to demonstrate the application interface and analysis workflow.

Planned screenshots:

Home page
Registration page
Login page
Image upload page
Facial analysis result
Generated report
Demo

A complete project demonstration will be added after the application workflow is finalized.

The planned demonstration will cover:

Registration
     |
     v
Login
     |
     v
Image Upload
     |
     v
Facial Analysis
     |
     v
Beauty Score
     |
     v
Analysis Results
     |
     v
Report Generation
Database

The application uses SQLite with SQLAlchemy.

The database is used for application data such as:

User information
Authentication-related data
Uploaded image information

The local database file is intentionally excluded from Git using .gitignore.

Security and Data Handling

The repository intentionally does not track:

Environment files
API keys and secrets
Local SQLite databases
Uploaded images
Processed images
Generated reports
Python cache files
Virtual environments
Local datasets

Sensitive configuration values should be stored in environment variables and should never be committed to GitHub.

Current Project Status
Completed
Backend setup
Face detection
Beauty score calculation
Facial feature analysis
Facial analysis and beauty report
FastAPI REST API
SQLite database integration
User registration and login
Password hashing
Web frontend
Planned
Analysis history
Hairstyle recommendations
Glasses recommendations
Makeup recommendations
Personalized beauty tips
Celebrity look-alike analysis
Improved AI models
Cloud deployment
Generative AI integration
Future Improvements

Future versions may include:

Analysis history for registered users
Personalized hairstyle recommendations
Glasses recommendations based on face shape
Makeup recommendations
AI-generated personalized beauty tips
Improved facial analysis models
Model optimization
Cloud deployment
Production-ready authentication
Better frontend user experience
Generative AI-based recommendations
Learning Outcomes

This project demonstrates practical experience with:

Computer vision
Facial landmark processing
Image analysis
Python application development
REST API development
FastAPI
SQLAlchemy
SQLite
Authentication
Frontend-backend integration
Git and GitHub
AI project architecture
End-to-end application development
Author

Ayushi Ahire

AI/ML Student focused on:

Machine Learning
Deep Learning
Computer Vision
Generative AI
MLOps
Data Engineering
Connect

GitHub: https://github.com/ayushiahire139-sudo

LinkedIn: https://www.linkedin.com/in/ayushi-ahire-462686319/

Project Repository

https://github.com/ayushiahire139-sudo/AI_Facial_Beauty_Analyzer