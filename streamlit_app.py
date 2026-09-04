import streamlit as st
import sys
import os
import time
import base64
import cv2
import numpy as np
from PIL import Image

# Add backend directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

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
    page_title="AI Facial Beauty Analyzer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# Theme Styles Configuration
# ----------------------------------------------------
THEMES = {
    "Hologram Glass": {
        "body_bg": "radial-gradient(circle at 10% 20%, #1e1b4b 0%, #0f172a 90%)",
        "card_bg": "rgba(30, 41, 59, 0.65)",
        "card_border": "1px solid rgba(255, 255, 255, 0.12)",
        "text_color": "#f8fafc",
        "text_muted": "#94a3b8",
        "primary": "#8b5cf6",
        "primary_gradient": "linear-gradient(135deg, #8b5cf6, #ec4899)",
        "accent": "#ec4899",
        "shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.45)",
        "font": "'Outfit', sans-serif"
    },
    "Cyberpunk Glow": {
        "body_bg": "linear-gradient(135deg, #050505 0%, #0c0a0f 100%)",
        "card_bg": "rgba(10, 10, 15, 0.9)",
        "card_border": "2px solid #00f0ff",
        "text_color": "#00ffcc",
        "text_muted": "#8b9bb4",
        "primary": "#ff007f",
        "primary_gradient": "linear-gradient(135deg, #ff007f, #00f0ff)",
        "accent": "#00f0ff",
        "shadow": "0 0 20px rgba(0, 240, 255, 0.3)",
        "font": "'Space Grotesk', sans-serif"
    },
    "Luxury Orchid": {
        "body_bg": "radial-gradient(circle at 50% 50%, #faf8f6 0%, #eae5e0 100%)",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "card_border": "1px solid rgba(76, 29, 149, 0.15)",
        "text_color": "#2e1065",
        "text_muted": "#6b21a8",
        "primary": "#4c1d95",
        "primary_gradient": "linear-gradient(135deg, #4c1d95, #d97706)",
        "accent": "#d97706",
        "shadow": "0 10px 40px rgba(76, 29, 149, 0.08)",
        "font": "'Playfair Display', serif"
    },
    "Emerald Serene": {
        "body_bg": "linear-gradient(135deg, #02120b 0%, #062417 100%)",
        "card_bg": "rgba(6, 36, 23, 0.75)",
        "card_border": "1px solid rgba(16, 185, 129, 0.2)",
        "text_color": "#ecfdf5",
        "text_muted": "#6ee7b7",
        "primary": "#10b981",
        "primary_gradient": "linear-gradient(135deg, #10b981, #06b6d4)",
        "accent": "#06b6d4",
        "shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.5)",
        "font": "'Outfit', sans-serif"
    }
}

# Sidebar Theme Selector
with st.sidebar:
    st.markdown("### 🎨 Visual Theme")
    selected_theme_name = st.selectbox(
        "Choose Interface Theme:",
        list(THEMES.keys()),
        index=0
    )
    theme = THEMES[selected_theme_name]
    
    st.divider()
    st.markdown("### 🔬 System Engine")
    st.markdown("""
    - **468 3D Dense Mesh Landmarks**
    - **Random Forest Regressor** Beauty Engine
    - **Golden Ratio & Symmetry Analysis**
    - **Auto-Rotation & Scale Normalizer**
    - **Clinical Aesthetic PDF Generation**
    """)
    st.divider()
    st.caption("AI Facial Beauty Analyzer v2.0 • Full-Stack AI")

# Inject Custom CSS Matching Previous Frontend
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    .stApp {{
        background: {theme['body_bg']} !important;
        color: {theme['text_color']} !important;
        font-family: {theme['font']};
    }}
    
    /* Top Navbar */
    .custom-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: {theme['card_bg']};
        backdrop-filter: blur(12px);
        border: {theme['card_border']};
        border-radius: 16px;
        box-shadow: {theme['shadow']};
        margin-bottom: 2rem;
    }}
    
    .nav-logo {{
        font-size: 1.5rem;
        font-weight: 800;
        background: {theme['primary_gradient']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .nav-badges {{
        display: flex;
        gap: 0.8rem;
    }}
    
    .badge {{
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        color: {theme['text_color']};
    }}
    
    /* Hero Header */
    .hero-box {{
        background: {theme['card_bg']};
        backdrop-filter: blur(12px);
        border: {theme['card_border']};
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: {theme['shadow']};
        margin-bottom: 2rem;
    }}
    
    .hero-box h1 {{
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
        background: {theme['primary_gradient']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .hero-box p {{
        font-size: 1.15rem;
        color: {theme['text_muted']};
        max-width: 750px;
        margin: 0 auto;
        line-height: 1.6;
    }}
    
    /* Card Component */
    .glass-card {{
        background: {theme['card_bg']};
        backdrop-filter: blur(12px);
        border: {theme['card_border']};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: {theme['shadow']};
        margin-bottom: 1.5rem;
    }}
    
    .score-circle {{
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: {theme['card_bg']};
        border: 4px solid {theme['primary']};
        box-shadow: 0 0 20px {theme['primary']};
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 auto 1rem auto;
    }}
    
    .score-number {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {theme['text_color']};
        line-height: 1;
    }}
    
    .score-sub {{
        font-size: 0.8rem;
        color: {theme['text_muted']};
    }}
    
    .metric-grid-card {{
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }}
    
    .metric-grid-val {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {theme['primary']};
    }}
    
    .metric-grid-lbl {{
        font-size: 0.85rem;
        color: {theme['text_muted']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }}
    
    .rec-box {{
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid {theme['primary']};
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        color: {theme['text_color']};
    }}
    
    .rec-box b {{
        color: {theme['accent']};
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Top Navigation Bar
# ----------------------------------------------------
st.markdown(f"""
<div class="custom-nav">
    <div class="nav-logo">✨ AI Facial Beauty Analyzer</div>
    <div class="nav-badges">
        <span class="badge">468 3D Mesh</span>
        <span class="badge">ML Beauty Engine</span>
        <span class="badge">Theme: {selected_theme_name}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Hero Section
# ----------------------------------------------------
st.markdown("""
<div class="hero-box">
    <h1>Discover Your Facial Geometry & Proportions</h1>
    <p>Upload a front-facing portrait to analyze 3D landmark mesh alignment, calculate golden ratio harmony, evaluate symmetry, and generate clinical aesthetic PDF reports.</p>
</div>
""", unsafe_allow_html=True)

# Create folders
TEMP_UPLOADS = os.path.join(BASE_DIR, "uploads")
TEMP_PROCESSED = os.path.join(BASE_DIR, "processed_images")
TEMP_REPORTS = os.path.join(BASE_DIR, "reports")

os.makedirs(TEMP_UPLOADS, exist_ok=True)
os.makedirs(TEMP_PROCESSED, exist_ok=True)
os.makedirs(TEMP_REPORTS, exist_ok=True)

# ----------------------------------------------------
# Upload Section
# ----------------------------------------------------
col_upload, col_preview = st.columns([1.2, 1])

with col_upload:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📤 Upload Portrait Photo")
    uploaded_file = st.file_uploader(
        "Choose a high-resolution front-facing face portrait:",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    st.caption("Supported formats: JPEG, PNG, WEBP (Smartphone & Camera portraits supported)")
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    temp_input_path = os.path.join(TEMP_UPLOADS, f"upload_{uploaded_file.name}")
    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    temp_output_path = os.path.join(TEMP_PROCESSED, f"landmarks_{uploaded_file.name}")
    
    with col_preview:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📷 Image Preview")
        st.image(temp_input_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("✨ Begin AI Face Analysis", type="primary", use_container_width=True)
    
    if run_btn:
        with st.spinner("🔍 Extracting 468 3D landmarks, checking auto-rotation, and computing geometric scores..."):
            # 1. Landmark Detection
            output_image_path, landmarks = detect_landmarks(temp_input_path, temp_output_path)
            
            # 2. Geometric & ML Scores
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
            
            # 3. Recommendations & Report
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
            
            # 4. Generate PDF Report with Embedded Face Mapping
            timestamp = int(time.time())
            pdf_filename = f"beauty_report_{timestamp}.pdf"
            pdf_path = generate_pdf_report(
                beauty_report,
                pdf_filename,
                original_image_path=temp_input_path,
                landmarks_image_path=temp_output_path
            )
            
        st.success("✅ Analysis Complete!")
        
        # ----------------------------------------------------
        # Score Cards (Matching Previous Frontend)
        # ----------------------------------------------------
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; margin-top: 1.5rem;">
            <div class="score-circle">
                <div class="score-number">{beauty_score}</div>
                <div class="score-sub">/ 100 SCORE</div>
            </div>
            <h2 style="margin: 0; color: {theme['primary']};">Facial Harmony & Beauty Index</h2>
            <p style="color: {theme['text_muted']}; margin-top: 0.3rem;">Evaluated using Random Forest Regressor & Multi-Point 3D Geometry</p>
        </div>
        """, unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-grid-card">
                <div class="metric-grid-val">{symmetry_score}%</div>
                <div class="metric-grid-lbl">Global Symmetry</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-grid-card">
                <div class="metric-grid-val">{golden_ratio_score}%</div>
                <div class="metric-grid-lbl">Golden Ratio</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-grid-card">
                <div class="metric-grid-val" style="font-size: 1.5rem;">{face_shape}</div>
                <div class="metric-grid-lbl">Face Shape</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-grid-card">
                <div class="metric-grid-val" style="font-size: 1.5rem;">{estimated_age}</div>
                <div class="metric-grid-lbl">Estimated Age</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ----------------------------------------------------
        # Visual Landmark Face Mapping (Side-by-Side Comparison)
        # ----------------------------------------------------
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="margin-top: 0; color: {theme['primary']};">👁️ Visual Face Mapping & 468-Point Mesh Overlay</h3>
            <p style="color: {theme['text_muted']};">Compare your original portrait with the high-density 3D facial landmark mesh used for symmetry and proportion calculations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        v1, v2 = st.columns(2)
        with v1:
            st.subheader("📷 Original Portrait")
            st.image(temp_input_path, use_container_width=True)
        with v2:
            st.subheader("🕸️ 3D Facial Landmark Mesh (468 Points)")
            st.image(temp_output_path, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ----------------------------------------------------
        # Feature Details & Recommendations
        # ----------------------------------------------------
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: {theme['primary']};">📐 Facial Proportions Breakdown</h3>
                <p><b>👤 Demographic Profile:</b> Gender: {gender} | Skin Tone: {skin_tone} | Emotion: {emotion}</p>
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 1rem 0;">
                <p><b>👁️ Eyes:</b> Distance: <code>{eye_analysis['eye_distance']}</code> | Symmetry: <code>{eye_analysis['eye_symmetry']}</code></p>
                <p><b>👃 Nose:</b> Width: <code>{nose_analysis['nose_width']}</code> | Shape: <code>{nose_analysis['nose_shape']}</code></p>
                <p><b>👄 Lips:</b> Width: <code>{lip_analysis['lip_width']}</code> | Shape: <code>{lip_analysis['lip_shape']}</code></p>
                <p><b>🦴 Jawline:</b> Width: <code>{jaw_analysis['jaw_width']}</code> | Shape: <code>{jaw_analysis['jaw_shape']}</code></p>
            </div>
            """, unsafe_allow_html=True)
            
        with r2:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: {theme['primary']};">💡 AI Personalized Beauty & Styling Guidelines</h3>
                <div class="rec-box">
                    <b>🧴 Skincare & Hydration:</b><br>{recommendations.get('skincare')}
                </div>
                <div class="rec-box">
                    <b>💇 Hairstyle & Contours:</b><br>{recommendations.get('hairstyle')}
                </div>
                <div class="rec-box">
                    <b>💄 Cosmetics & Accentuation:</b><br>{recommendations.get('makeup')}
                </div>
                <div class="rec-box">
                    <b>🥗 Wellness & Lifestyle:</b><br>{recommendations.get('lifestyle')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ----------------------------------------------------
        # Download Clinical PDF Report Button
        # ----------------------------------------------------
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3 style="color: {theme['primary']};">📥 Download Official Aesthetic PDF Report</h3>
            <p style="color: {theme['text_muted']};">Export your complete analysis with embedded face mapping diagrams, proportions table, and personalized recommendations as a clinical aesthetic PDF.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="📄 Download Full Aesthetic Analysis PDF Report",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
else:
    st.info("👆 Please upload a clear front-facing portrait photo to start the facial beauty analysis.")
