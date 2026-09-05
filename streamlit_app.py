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

import models
from database import engine, SessionLocal
from security import hash_password, verify_password

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

# Ensure SQLite Database Tables Exist
models.Base.metadata.create_all(bind=engine)

# Page Config
st.set_page_config(
    page_title="AI Facial Beauty Analyzer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""

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

# Sidebar
with st.sidebar:
    st.markdown("### 🎨 Visual Theme")
    selected_theme_name = st.selectbox(
        "Choose Interface Theme:",
        list(THEMES.keys()),
        index=0
    )
    theme = THEMES[selected_theme_name]
    
    st.divider()
    if st.session_state["authenticated"]:
        st.markdown(f"### 👤 Active Account")
        st.write(f"**Name:** {st.session_state['user_name']}")
        if st.session_state["user_email"]:
            st.write(f"**Email:** {st.session_state['user_email']}")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["user_name"] = ""
            st.session_state["user_email"] = ""
            st.rerun()
        st.divider()

    st.markdown("### 🔬 System Engine")
    st.markdown("""
    - **468 3D Dense Mesh Landmarks**
    - **UTKFace Ensemble ML Engine**
    - **Dual-Stream Wrinkle Texture Analyzer**
    - **Golden Ratio & Symmetry Analysis**
    - **Clinical Aesthetic PDF Generation**
    """)
    st.divider()
    st.caption("AI Facial Beauty Analyzer v2.0 • Full-Stack AI")

# Inject Custom CSS Matching Previous Frontend
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Completely Hide GitHub Icon, Header Toolbar, and Streamlit Branding */
    #MainMenu {{visibility: hidden !important; display: none !important;}}
    header {{visibility: hidden !important; height: 0 !important; display: none !important;}}
    footer {{visibility: hidden !important; display: none !important;}}
    .stAppDeployButton {{display: none !important;}}
    [data-testid="stToolbar"] {{display: none !important; visibility: hidden !important;}}
    [data-testid="stDecoration"] {{display: none !important; visibility: hidden !important;}}
    [data-testid="stStatusWidget"] {{display: none !important; visibility: hidden !important;}}
    [data-testid="stHeader"] {{display: none !important; visibility: hidden !important;}}
    
    .stApp {{
        background: {theme['body_bg']} !important;
        color: {theme['text_color']} !important;
        font-family: {theme['font']};
        padding-top: 1rem !important;
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
    
    /* Sleek & Efficient File Uploader Styling */
    [data-testid="stFileUploader"] {{
        background: {theme['card_bg']} !important;
        border: {theme['card_border']} !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: {theme['shadow']} !important;
        backdrop-filter: blur(12px) !important;
    }}
    
    [data-testid="stFileUploader"] section {{
        background: rgba(15, 23, 42, 0.4) !important;
        border: 2px dashed {theme['primary']} !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease;
    }}
    
    [data-testid="stFileUploader"] section:hover {{
        border-color: {theme['accent']} !important;
        transform: translateY(-2px);
    }}
    
    [data-testid="stFileUploader"] small {{
        color: {theme['text_muted']} !important;
    }}
    
    /* Primary Action Buttons */
    .stButton > button {{
        background: {theme['primary_gradient']} !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 0.75rem 1.8rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4) !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 30px rgba(236, 72, 153, 0.5) !important;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# AUTHENTICATION GUARD: LOGIN & REGISTRATION FIRST
# ----------------------------------------------------
if not st.session_state["authenticated"]:
    st.markdown(f"""
    <div class="custom-nav">
        <div class="nav-logo">✨ AI Facial Beauty Analyzer</div>
        <div class="nav-badges">
            <span class="badge">🔒 User Portal</span>
            <span class="badge">Theme: {selected_theme_name}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-box">
        <h1>Welcome to AI Facial Beauty Analyzer</h1>
        <p>Sign in or register a free account to unlock deep learning 468-point 3D facial mapping, golden ratio calculations, and clinical aesthetic PDF reports.</p>
    </div>
    """, unsafe_allow_html=True)

    col_center = st.columns([1, 1.8, 1])[1]
    
    with col_center:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["🔐 Sign In", "📝 Create New Account (Register)"])
        
        # --- TAB 1: SIGN IN ---
        with tab_login:
            st.markdown(f"<h3 style='color:{theme['primary']}; margin-top:0;'>Access Your Dashboard</h3>", unsafe_allow_html=True)
            login_email = st.text_input("Email Address", key="login_email_input", placeholder="name@example.com")
            login_password = st.text_input("Password", type="password", key="login_password_input", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In to Analyzer ✨", key="login_btn", use_container_width=True):
                if not login_email or not login_password:
                    st.error("Please enter both email and password.")
                else:
                    db = SessionLocal()
                    try:
                        user = db.query(models.User).filter(models.User.email == login_email.strip().lower()).first()
                        if user and verify_password(login_password, user.password):
                            st.session_state["authenticated"] = True
                            st.session_state["user_name"] = user.fullname
                            st.session_state["user_email"] = user.email
                            st.success(f"Welcome back, {user.fullname}!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Invalid email or password. Please try again.")
                    finally:
                        db.close()
                        
            st.divider()
            st.markdown("<p style='text-align:center; font-size:0.85rem;'>Need instant evaluation?</p>", unsafe_allow_html=True)
            if st.button("⚡ Quick Guest Access (Demo)", key="guest_btn", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = "Guest User"
                st.session_state["user_email"] = "guest@analyzer.ai"
                st.rerun()

        # --- TAB 2: REGISTER ---
        with tab_register:
            st.markdown(f"<h3 style='color:{theme['accent']}; margin-top:0;'>Register Your Account</h3>", unsafe_allow_html=True)
            reg_fullname = st.text_input("Full Name", key="reg_fullname_input", placeholder="John Doe / Ayushi Ahire")
            reg_email = st.text_input("Email Address", key="reg_email_input", placeholder="name@example.com")
            reg_password = st.text_input("Create Password", type="password", key="reg_password_input", placeholder="At least 6 characters")
            reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password_input", placeholder="Repeat your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register & Get Started 🚀", key="reg_btn", use_container_width=True):
                if not reg_fullname or not reg_email or not reg_password:
                    st.error("Please fill in all registration fields.")
                elif reg_password != reg_confirm_password:
                    st.error("Passwords do not match. Please re-enter.")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    db = SessionLocal()
                    try:
                        existing = db.query(models.User).filter(models.User.email == reg_email.strip().lower()).first()
                        if existing:
                            st.error("An account with this email already exists. Please Sign In.")
                        else:
                            hashed_pwd = hash_password(reg_password)
                            new_user = models.User(
                                fullname=reg_fullname.strip(),
                                email=reg_email.strip().lower(),
                                password=hashed_pwd
                            )
                            db.add(new_user)
                            db.commit()
                            
                            st.session_state["authenticated"] = True
                            st.session_state["user_name"] = reg_fullname.strip()
                            st.session_state["user_email"] = reg_email.strip().lower()
                            st.success("Account registered successfully! Redirecting...")
                            time.sleep(0.5)
                            st.rerun()
                    except Exception as e:
                        db.rollback()
                        st.error(f"Registration error: {e}")
                    finally:
                        db.close()
                        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ----------------------------------------------------
# MAIN APPLICATION DASHBOARD (UNLOCKED AFTER LOGIN)
# ----------------------------------------------------
st.markdown(f"""
<div class="custom-nav">
    <div class="nav-logo">✨ AI Facial Beauty Analyzer</div>
    <div class="nav-badges">
        <span class="badge">👤 {st.session_state['user_name']}</span>
        <span class="badge">468 3D Mesh</span>
        <span class="badge">Theme: {selected_theme_name}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
<div class="hero-box">
    <h1>Welcome, {st.session_state['user_name']}!</h1>
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
# Upload Section (Clean, Efficient & Integrated)
# ----------------------------------------------------
st.markdown(f"### 📤 Upload Portrait Photo")
uploaded_file = st.file_uploader(
    "Upload a clear front-facing portrait photo (JPG, PNG, WEBP):",
    type=["jpg", "jpeg", "png", "webp"],
    help="Smartphone & camera portraits are supported. Auto-rotation and proportion scaling will be applied automatically."
)

if uploaded_file is not None:
    temp_input_path = os.path.join(TEMP_UPLOADS, f"upload_{uploaded_file.name}")
    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    temp_output_path = os.path.join(TEMP_PROCESSED, f"landmarks_{uploaded_file.name}")
    
    col_img, col_act = st.columns([1, 1.2])
    with col_img:
        st.image(temp_input_path, caption="📷 Uploaded Face Preview", use_container_width=True)
        
    with col_act:
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: {theme['primary']}; margin-top:0;">Ready for AI Inspection</h3>
            <p style="color: {theme['text_muted']};">The AI engine will normalize orientation, map 468 facial coordinates, compute symmetry ratios, and generate recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
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
            estimated_age = estimate_age(landmarks, image_path=temp_input_path)
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
        # Score Breakdown & Detailed Findings (Matching Image 1)
        # ----------------------------------------------------
        col_sb1, col_sb2 = st.columns([1, 1.3])
        
        with col_sb1:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: {theme['primary']}; margin-top:0;">📊 Score Breakdown</h3>
            """, unsafe_allow_html=True)
            
            breakdown_dict = beauty_report.get("score_breakdown", {})
            for cat_name, cat_score in breakdown_dict.items():
                st.write(f"**{cat_name}** ({cat_score}/100)")
                st.progress(cat_score / 100.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_sb2:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: {theme['primary']}; margin-top:0;">📋 Detailed Findings</h3>
            """, unsafe_allow_html=True)
            findings_dict = beauty_report.get("detailed_findings", {})
            icon_map = {
                "symmetry": "⚖️", "proportions": "📏", "bone_structure": "👤",
                "skin_quality": "💧", "eyes": "👁️", "nose": "👃",
                "lips": "👄", "jawline_chin": "🦴"
            }
            for k, f_item in findings_dict.items():
                icon = icon_map.get(k, "•")
                title = f_item.get("title", k.capitalize())
                score = f_item.get("score", 70)
                text = f_item.get("text", "")
                st.markdown(f"""
                <div style="margin-bottom: 0.6rem; padding-bottom: 0.4rem; border-bottom: 1px solid rgba(255,255,255,0.06);">
                    <div style="display:flex; justify-content:space-between; font-weight:600;">
                        <span>{icon} {title}</span>
                        <span style="color:{theme['primary']};">{score} / 100</span>
                    </div>
                    <div style="font-size:0.85rem; color:{theme['text_muted']};">{text}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # ----------------------------------------------------
        # Key Strengths & Areas for Improvement (Matching Image 1)
        # ----------------------------------------------------
        col_str, col_imp = st.columns(2)
        with col_str:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: {theme['primary']}; margin-top:0;">🌟 Key Strengths</h3>
            """, unsafe_allow_html=True)
            for s in beauty_report.get("key_strengths", []):
                st.markdown(f"• **{s}**")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_imp:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: {theme['accent']}; margin-top:0;">🎯 Areas for Improvement</h3>
            """, unsafe_allow_html=True)
            for imp in beauty_report.get("areas_for_improvement", []):
                st.markdown(f"• **{imp}**")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # Grooming & Style Recommendations (5 Columns - Matching Image 1)
        # ----------------------------------------------------
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: {theme['primary']}; margin-top: 0;">✨ Grooming & Style Recommendations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        g1, g2, g3, g4, g5 = st.columns(5)
        grooming_dict = beauty_report.get("grooming_recommendations", {})
        
        with g1:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 180px;">
                <h4 style="color:{theme['primary']}; margin-top:0;">〰️ BROWS</h4>
                <p style="font-size:0.85rem; color:{theme['text_muted']};">• {grooming_dict.get('brows', [''])[0]}<br><br>• {grooming_dict.get('brows', ['',''])[1]}</p>
            </div>
            """, unsafe_allow_html=True)
        with g2:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 180px;">
                <h4 style="color:{theme['primary']}; margin-top:0;">👁️ EYES</h4>
                <p style="font-size:0.85rem; color:{theme['text_muted']};">• {grooming_dict.get('eyes', [''])[0]}<br><br>• {grooming_dict.get('eyes', ['',''])[1]}</p>
            </div>
            """, unsafe_allow_html=True)
        with g3:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 180px;">
                <h4 style="color:{theme['primary']}; margin-top:0;">👤 CONTOUR</h4>
                <p style="font-size:0.85rem; color:{theme['text_muted']};">• {grooming_dict.get('contour_face', [''])[0]}<br><br>• {grooming_dict.get('contour_face', ['',''])[1]}</p>
            </div>
            """, unsafe_allow_html=True)
        with g4:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 180px;">
                <h4 style="color:{theme['primary']}; margin-top:0;">👄 LIPS</h4>
                <p style="font-size:0.85rem; color:{theme['text_muted']};">• {grooming_dict.get('lips', [''])[0]}<br><br>• {grooming_dict.get('lips', ['',''])[1]}</p>
            </div>
            """, unsafe_allow_html=True)
        with g5:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 180px;">
                <h4 style="color:{theme['primary']}; margin-top:0;">💇 HAIR</h4>
                <p style="font-size:0.85rem; color:{theme['text_muted']};">• {grooming_dict.get('hair', [''])[0]}<br><br>• {grooming_dict.get('hair', ['',''])[1]}</p>
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
        # Download Clinical PDF Report Button (Exact Image 1 Match)
        # ----------------------------------------------------
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3 style="color: {theme['primary']};">📥 Download Official Clinical Facial Beauty Report (PDF)</h3>
            <p style="color: {theme['text_muted']};">Download your high-resolution clinical aesthetic report featuring the exact editorial score breakdowns, detailed findings, 3D face mesh, and grooming recommendations matching the official standard.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="📄 Download Clinical Facial Beauty Report (PDF)",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
