import streamlit as st
import sys
import os
import time
import cv2
import numpy as np
from PIL import Image

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from landmark_detector import detect_landmarks
from beauty_score import calculate_beauty_score
from symmetry import calculate_symmetry
from golden_ratio import calculate_golden_ratio
from face_shape import detect_face_shape
from skin_tone import detect_skin_tone
from age_estimation import estimate_age
from gender_detection import detect_gender
from emotion_detection import detect_emotion
from eye_analysis import analyze_eyes
from nose_analysis import analyze_nose
from lip_analysis import analyze_lips
from jaw_analysis import analyze_jaw
from beauty_report import generate_beauty_report
from recommendation_engine import generate_recommendations
from report_generator import generate_pdf_report

# Page Config
st.set_page_config(
    page_title="AI Facial Beauty & Landmark Analyzer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #4C1D95 0%, #7C3AED 50%, #C084FC 100%);
        padding: 2.2rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.25);
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .metric-box {
        background: #F5F3FF;
        border: 1px solid #DDD6FE;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.08);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #4C1D95;
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #7C3AED;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .rec-card {
        background: #FAF5FF;
        border-left: 4px solid #8B5CF6;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="main-header">
    <h1>✨ AI Facial Beauty & Landmark Analyzer</h1>
    <p>Real-time 468-Point 3D Facial Mapping, Random Forest Beauty Regression, Geometric Proportions & Aesthetic PDF Reports</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80", caption="Facial Geometry & Beauty AI")
    st.markdown("### 🔬 System Capabilities")
    st.markdown("""
    - **468 3D Dense Mesh Landmarks** (MediaPipe)
    - **Random Forest Regressor** Beauty Engine
    - **Golden Ratio & Symmetry Analysis**
    - **Auto-Rotation & Scale Normalizer**
    - **Clinical Aesthetic PDF Generation**
    """)
    st.divider()
    st.markdown("Developed with FastAPI, MediaPipe, Scikit-Learn & Streamlit")

# Temporary Directories Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_UPLOADS = os.path.join(BASE_DIR, "uploads")
TEMP_PROCESSED = os.path.join(BASE_DIR, "processed_images")
TEMP_REPORTS = os.path.join(BASE_DIR, "reports")

os.makedirs(TEMP_UPLOADS, exist_ok=True)
os.makedirs(TEMP_PROCESSED, exist_ok=True)
os.makedirs(TEMP_REPORTS, exist_ok=True)

# File Uploader
uploaded_file = st.file_uploader(
    "📸 Upload a front-facing portrait photo (JPG, JPEG, PNG, WEBP):",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:
    # Save input file
    temp_input_path = os.path.join(TEMP_UPLOADS, f"upload_{uploaded_file.name}")
    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    temp_output_path = os.path.join(TEMP_PROCESSED, f"landmarks_{uploaded_file.name}")
    
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        analyze_btn = st.button("✨ Begin AI Face Analysis", type="primary", use_container_width=True)
        
    if analyze_btn:
        with st.spinner("🔍 Running 468-point 3D landmark mapping and beauty regressor..."):
            # 1. Detect Landmarks with auto-rotation correction
            output_image_path, landmarks = detect_landmarks(temp_input_path, temp_output_path)
            
            # 2. Run Geometric & ML Analysis
            symmetry_score = calculate_symmetry(landmarks)
            beauty_score = calculate_beauty_score(landmarks, symmetry_score)
            face_shape = detect_face_shape(landmarks)
            golden_ratio_score = calculate_golden_ratio(landmarks)
            
            eye_analysis = analyze_eyes(landmarks)
            nose_analysis = analyze_nose(landmarks)
            lip_analysis = analyze_lips(landmarks)
            jaw_analysis = analyze_jaw(landmarks)
            
            skin_tone = detect_skin_tone(temp_input_path)
            estimated_age = estimate_age(landmarks)
            gender = detect_gender(landmarks)
            emotion = detect_emotion(landmarks)
            
            # 3. Generate Reports & Recommendations
            beauty_report = generate_beauty_report(
                beauty_score, symmetry_score, face_shape, golden_ratio_score,
                eye_analysis, nose_analysis, lip_analysis, jaw_analysis,
                skin_tone, estimated_age, gender, emotion
            )
            
            recommendations = generate_recommendations(
                beauty_score, face_shape, eye_analysis, nose_analysis,
                lip_analysis, jaw_analysis, skin_tone, emotion
            )
            beauty_report["recommendations"] = recommendations
            
            # 4. Generate PDF Report with face mapping embedded
            timestamp = int(time.time())
            pdf_filename = f"beauty_report_{timestamp}.pdf"
            pdf_path = generate_pdf_report(
                beauty_report,
                pdf_filename,
                original_image_path=temp_input_path,
                landmarks_image_path=temp_output_path
            )
            
        st.success("✅ Facial Analysis Completed Successfully!")
        
        # ----------------------------------------------------
        # Score Summary Cards
        # ----------------------------------------------------
        st.markdown("### 📊 Overall Score Summary")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Beauty Harmony</div>
                <div class="metric-value">{beauty_score}/100</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Global Symmetry</div>
                <div class="metric-value">{symmetry_score}/100</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Golden Ratio</div>
                <div class="metric-value">{golden_ratio_score}/100</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Face Shape</div>
                <div class="metric-value" style="font-size:1.6rem; padding-top:0.3rem;">{face_shape}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ----------------------------------------------------
        # Visual Face Mapping Side-by-Side
        # ----------------------------------------------------
        st.markdown("### 👁️ Visual Face Mapping & Alignment")
        v1, v2 = st.columns(2)
        with v1:
            st.subheader("📷 Original Portrait")
            st.image(temp_input_path, use_container_width=True)
        with v2:
            st.subheader("🕸️ 3D Landmark Mesh (468 Points)")
            st.image(temp_output_path, use_container_width=True)
            
        st.divider()
        
        # ----------------------------------------------------
        # Profile & Feature Details
        # ----------------------------------------------------
        f1, f2 = st.columns(2)
        with f1:
            st.markdown("### 👤 Profile Demographics")
            st.write(f"**Estimated Age:** {estimated_age}")
            st.write(f"**Skin Tone:** {skin_tone}")
            st.write(f"**Gender Profile:** {gender}")
            st.write(f"**Detected Emotion:** {emotion}")
            
            st.markdown("### 📐 Proportional Feature Analysis")
            st.write(f"**Eyes:** Distance: `{eye_analysis['eye_distance']}` | Symmetry: `{eye_analysis['eye_symmetry']}`")
            st.write(f"**Nose:** Width: `{nose_analysis['nose_width']}` | Shape: `{nose_analysis['nose_shape']}`")
            st.write(f"**Lips:** Width: `{lip_analysis['lip_width']}` | Shape: `{lip_analysis['lip_shape']}`")
            st.write(f"**Jaw:** Width: `{jaw_analysis['jaw_width']}` | Shape: `{jaw_analysis['jaw_shape']}`")
            
        with f2:
            st.markdown("### 💡 AI Personalized Guidelines")
            st.markdown(f"""
            <div class="rec-card">
                <b>🧴 Skincare & Hydration:</b><br>{recommendations.get('skincare')}
            </div>
            <div class="rec-card">
                <b>💇 Hairstyle & Contours:</b><br>{recommendations.get('hairstyle')}
            </div>
            <div class="rec-card">
                <b>💄 Cosmetics & Accentuation:</b><br>{recommendations.get('makeup')}
            </div>
            <div class="rec-card">
                <b>🥗 Wellness & Lifestyle:</b><br>{recommendations.get('lifestyle')}
            </div>
            """, unsafe_allow_html=True)
            
        st.divider()
        
        # ----------------------------------------------------
        # Download PDF Report Button
        # ----------------------------------------------------
        st.markdown("### 📥 Download Clinical Aesthetic PDF Report")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="📄 Download Aesthetic Face Analysis PDF Report",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    type="primary"
                )
else:
    st.info("👆 Please upload a clear, front-facing portrait photo to start the facial beauty analysis.")
