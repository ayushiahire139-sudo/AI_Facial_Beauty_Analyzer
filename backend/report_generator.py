import os
import time
from datetime import datetime
from PIL import Image as PILImage, ImageDraw

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing, Circle, String, Rect, Line, Group

def get_scaled_reportlab_image(image_path, max_width=200, max_height=180):
    """
    Safely loads and proportionally scales an image for ReportLab PDF embedding.
    """
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        with PILImage.open(image_path) as img:
            w, h = img.size
            if w <= 0 or h <= 0:
                return None
            ratio = min(max_width / float(w), max_height / float(h))
            new_w = w * ratio
            new_h = h * ratio
            return RLImage(image_path, width=new_w, height=new_h)
    except Exception as e:
        print(f"Error scaling image '{image_path}': {e}")
        return None

def create_score_donut_drawing(score, label="ABOVE AVERAGE"):
    """
    Draws a clean, clinical monochrome circular score donut.
    """
    d = Drawing(120, 100)
    # Outer ring
    d.add(Circle(60, 52, 40, strokeColor=colors.HexColor("#111111"), strokeWidth=4.5, fillColor=colors.HexColor("#FFFFFF")))
    # Inner number
    d.add(String(60, 52, str(int(round(score))), fontName="Helvetica-Bold", fontSize=26, textAnchor="middle", fillColor=colors.HexColor("#111111")))
    # Subtitle / 100
    d.add(String(60, 36, "/ 100", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor("#666666")))
    # Label
    d.add(String(60, 8, label.upper(), fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=colors.HexColor("#111111")))
    return d

def create_bar_cell(score_val):
    """
    Draws a clean horizontal progress bar.
    """
    d = Drawing(65, 8)
    # Background track
    d.add(Rect(0, 1, 60, 5, fillColor=colors.HexColor("#E2E8F0"), strokeColor=None, rx=2, ry=2))
    # Filled bar
    fill_w = max(5, min(60, 60 * (float(score_val) / 100.0)))
    d.add(Rect(0, 1, fill_w, 5, fillColor=colors.HexColor("#111111"), strokeColor=None, rx=2, ry=2))
    return d

def generate_pdf_report(report_data, filename, original_image_path=None, landmarks_image_path=None):
    """
    Generates the Clinical Aesthetic Facial Beauty Report matching the exact
    editorial monochrome benchmark (FACIAL BEAUTY REPORT).
    """
    reports_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    os.makedirs(reports_folder, exist_ok=True)
    pdf_path = os.path.join(reports_folder, filename)

    # 0.35-inch margins to fit the rich 1-page clinical layout cleanly
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=26,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    # Custom Clean Editorial Typography
    title_style = ParagraphStyle('RepTitle', fontName='Times-Bold', fontSize=18, leading=20, textColor=colors.HexColor("#111111"))
    subtitle_style = ParagraphStyle('RepSubtitle', fontName='Helvetica', fontSize=7, leading=9, textColor=colors.HexColor("#555555"))
    meta_style = ParagraphStyle('RepMeta', fontName='Helvetica', fontSize=7, leading=9, textColor=colors.HexColor("#444444"), alignment=2)
    meta_bold = ParagraphStyle('RepMetaB', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=colors.HexColor("#111111"))

    section_header = ParagraphStyle('SecHead', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#111111"))
    card_title = ParagraphStyle('CardTitle', fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=colors.HexColor("#111111"))
    card_body = ParagraphStyle('CardBody', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor("#444444"))
    card_bullet = ParagraphStyle('CardBullet', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor("#333333"))
    score_txt = ParagraphStyle('ScoreTxt', fontName='Helvetica-Bold', fontSize=7, leading=8.5, textColor=colors.HexColor("#111111"), alignment=2)
    footer_notes = ParagraphStyle('FootNotes', fontName='Helvetica', fontSize=5.5, leading=7, textColor=colors.HexColor("#555555"))
    footer_bar_txt = ParagraphStyle('FootBar', fontName='Helvetica-Bold', fontSize=6, leading=7.5, textColor=colors.white, alignment=1)

    story = []

    # -------------------------------------------------------------------------
    # 1. HEADER SECTION
    # -------------------------------------------------------------------------
    today_str = datetime.now().strftime("%B %d, %Y")
    report_id_str = f"FB-{datetime.now().strftime('%m%d%Y')}-{int(time.time()) % 100:02d}"

    header_left = [
        Paragraph("FACIAL BEAUTY REPORT", title_style),
        Spacer(1, 2),
        Paragraph("A DATA-DRIVEN ANALYSIS OF HARMONY &amp; AESTHETICS", subtitle_style)
    ]
    header_right = [
        Paragraph(f"<b>DATE:</b> &nbsp; {today_str}", meta_style),
        Paragraph(f"<b>REPORT ID:</b> &nbsp; {report_id_str}", meta_style),
        Paragraph(f"<b>METHOD:</b> &nbsp; Facial Geometry &amp; 3D Mesh", meta_style)
    ]

    header_table = Table([[header_left, header_right]], colWidths=[330, 226])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor("#111111")),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------------------
    # 2. ROW 1: USER PORTRAIT (LEFT) + OVERALL ATTRACTIVENESS SCORE (RIGHT)
    # -------------------------------------------------------------------------
    user_img = get_scaled_reportlab_image(original_image_path, max_width=245, max_height=145)
    if not user_img and landmarks_image_path:
        user_img = get_scaled_reportlab_image(landmarks_image_path, max_width=245, max_height=145)
    if not user_img:
        user_img = Paragraph("<i>Portrait Photo</i>", card_body)

    # Right Card: Score Breakdown Table
    b_score = report_data.get("beauty_score", 75)
    label_txt = report_data.get("overall_label", "ABOVE AVERAGE")
    score_donut = create_score_donut_drawing(b_score, label_txt)

    breakdown_data = report_data.get("score_breakdown", {
        "Symmetry": int(report_data.get("symmetry_score", 70)),
        "Proportions": int(report_data.get("golden_ratio_score", 70)),
        "Bone Structure": 68,
        "Skin Quality": 72,
        "Eyes": 75,
        "Nose": 69,
        "Lips": 74,
        "Jawline & Chin": 68,
        "Overall Harmony": int(b_score)
    })

    sb_rows = [[Paragraph("<b>SCORE BREAKDOWN</b>", card_title), "", ""]]
    for k, v in breakdown_data.items():
        sb_rows.append([
            Paragraph(k, card_body),
            create_bar_cell(v),
            Paragraph(f"<b>{v}</b> <font color='#666'>/100</font>", score_txt)
        ])

    sb_table = Table(sb_rows, colWidths=[78, 65, 38])
    sb_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    score_card_content = [
        Paragraph("OVERALL ATTRACTIVENESS SCORE", section_header),
        Spacer(1, 4),
        Table([[score_donut, sb_table]], colWidths=[110, 185], style=[
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ])
    ]

    r1_table = Table([[user_img, score_card_content]], colWidths=[250, 306])
    r1_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (0,0), 0.75, colors.HexColor("#E2E8F0")),
        ('BOX', (1,0), (1,0), 0.75, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#FAFAFA")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FFFFFF")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(r1_table)
    story.append(Spacer(1, 5))

    # -------------------------------------------------------------------------
    # 3. ROW 2: FACIAL ANALYSIS (LEFT) + DETAILED FINDINGS (RIGHT)
    # -------------------------------------------------------------------------
    mesh_img = get_scaled_reportlab_image(landmarks_image_path, max_width=115, max_height=140)
    if not mesh_img:
        mesh_img = get_scaled_reportlab_image(original_image_path, max_width=115, max_height=140)

    face_shape_str = report_data.get("face_shape", "Oval / Oblong")
    analysis_callouts = [
        Paragraph("<b>Face Shape</b>", card_title),
        Paragraph(face_shape_str, card_body),
        Spacer(1, 3),
        Paragraph("<b>Symmetry</b>", card_title),
        Paragraph("Mild asymmetry (within normal range)", card_body),
        Spacer(1, 3),
        Paragraph("<b>Proportions</b>", card_title),
        Paragraph("Good vertical thirds alignment", card_body),
        Spacer(1, 3),
        Paragraph("<b>Feature Balance</b>", card_title),
        Paragraph("Well-balanced overall harmony", card_body),
    ]

    mesh_annotated_table = Table([[mesh_img, analysis_callouts]], colWidths=[120, 118])
    mesh_annotated_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    facial_analysis_content = [
        Paragraph("FACIAL ANALYSIS", section_header),
        Spacer(1, 3),
        mesh_annotated_table
    ]

    # Detailed Findings rows
    findings = report_data.get("detailed_findings", {})
    df_rows = [[Paragraph("DETAILED FINDINGS", section_header), ""]]
    
    icon_map = {
        "symmetry": "⚖️", "proportions": "📏", "bone_structure": "👤",
        "skin_quality": "💧", "eyes": "👁️", "nose": "👃",
        "lips": "👄", "jawline_chin": "🦴"
    }

    for key, f_dict in findings.items():
        title = f_dict.get("title", key.capitalize())
        desc = f_dict.get("text", "")
        f_score = f_dict.get("score", 70)
        icon = icon_map.get(key, "•")
        
        entry_p = Paragraph(f"<b>{icon} {title}</b><br/><font color='#555'>{desc}</font>", card_body)
        score_p = Paragraph(f"<b>{f_score}</b> <font color='#666'>/100</font>", score_txt)
        df_rows.append([entry_p, score_p])

    df_table = Table(df_rows, colWidths=[238, 48])
    df_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,1), (-1,-2), 0.3, colors.HexColor("#F1F5F9")),
    ]))

    r2_table = Table([[facial_analysis_content, df_table]], colWidths=[250, 306])
    r2_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (0,0), 0.75, colors.HexColor("#E2E8F0")),
        ('BOX', (1,0), (1,0), 0.75, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FFFFFF")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(r2_table)
    story.append(Spacer(1, 5))

    # -------------------------------------------------------------------------
    # 4. ROW 3: KEY STRENGTHS & AREAS FOR IMPROVEMENT
    # -------------------------------------------------------------------------
    strengths_items = report_data.get("key_strengths", [
        "Good overall facial harmony and bilateral balance",
        "Well-proportioned horizontal facial thirds alignment",
        "Expressive, symmetrical eye alignment",
        "Even, clear skin tone and complexion",
        "Balanced lip contour and proportions"
    ])
    improvements_items = report_data.get("areas_for_improvement", [
        "Enhance jawline and chin contour definition",
        "Hydration & brightness in under-eye area",
        "Eyebrow shaping for enhanced facial framing",
        "Subtle upper lip volume enhancement",
        "Strategic contouring for cheekbone elevation"
    ])

    str_content = [Paragraph("KEY STRENGTHS", section_header), Spacer(1, 2)]
    for s in strengths_items[:5]:
        str_content.append(Paragraph(f"• &nbsp; {s}", card_bullet))

    imp_content = [Paragraph("AREAS FOR IMPROVEMENT", section_header), Spacer(1, 2)]
    for imp in improvements_items[:5]:
        imp_content.append(Paragraph(f"• &nbsp; {imp}", card_bullet))

    r3_table = Table([[str_content, imp_content]], colWidths=[278, 278])
    r3_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#E2E8F0")),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(r3_table)
    story.append(Spacer(1, 5))

    # -------------------------------------------------------------------------
    # 5. ROW 4: GROOMING & STYLE RECOMMENDATIONS (5 COLUMNS)
    # -------------------------------------------------------------------------
    grooming = report_data.get("grooming_recommendations", {})
    brows_pts = grooming.get("brows", ["Maintain natural fullness", "Soft arch to lift expression"])
    eyes_pts = grooming.get("eyes", ["Brighten under-eyes with hydration", "Subtle eyeliner to define shape"])
    contour_pts = grooming.get("contour_face", ["Light contour under cheekbones", "Jawline definition with bronzer"])
    lips_pts = grooming.get("lips", ["Use tinted balm or soft matte lip", "Subtle lip plumper/gloss"])
    hair_pts = grooming.get("hair", ["Layers to frame face", "Sleek finish enhances symmetry"])

    def make_col(icon, title, points):
        c = [Paragraph(f"<b>{icon} {title}</b>", card_title), Spacer(1, 2)]
        for pt in points[:2]:
            c.append(Paragraph(f"• {pt}", card_bullet))
        return c

    c1 = make_col("〰️", "BROWS", brows_pts)
    c2 = make_col("👁️", "EYES", eyes_pts)
    c3 = make_col("👤", "CONTOUR &amp; FACE", contour_pts)
    c4 = make_col("👄", "LIPS", lips_pts)
    c5 = make_col("💇", "HAIR", hair_pts)

    r4_cols = Table([[c1, c2, c3, c4, c5]], colWidths=[108, 110, 114, 110, 114])
    r4_cols.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    r4_box = [
        Paragraph("GROOMING &amp; STYLE RECOMMENDATIONS", section_header),
        Spacer(1, 3),
        r4_cols
    ]

    r4_table = Table([[r4_box]], colWidths=[556])
    r4_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(r4_table)
    story.append(Spacer(1, 5))

    # -------------------------------------------------------------------------
    # 6. ROW 5: NOTES & SCORE GUIDE + BOTTOM BLACK BANNER
    # -------------------------------------------------------------------------
    notes_content = [
        Paragraph("<b>NOTES</b>", card_title),
        Paragraph("Scores are based on facial geometry, symmetry, and visual harmony. Beauty is subjective; this report is an analytical reference, not a definitive judgment.", footer_notes)
    ]

    score_guide_table = Table([
        [Paragraph("<b>SCORE GUIDE</b>", card_title), "", "", "", "", ""],
        [
            Paragraph("<b>90 - 100</b>", card_bullet), Paragraph("Exceptional", footer_notes),
            Paragraph("<b>70 - 79</b>", card_bullet), Paragraph("Above Average", footer_notes),
            Paragraph("<b>50 - 59</b>", card_bullet), Paragraph("Below Average", footer_notes)
        ],
        [
            Paragraph("<b>80 - 89</b>", card_bullet), Paragraph("Very Attractive", footer_notes),
            Paragraph("<b>60 - 69</b>", card_bullet), Paragraph("Average", footer_notes),
            Paragraph("<b>0 - 49</b>", card_bullet), Paragraph("Low", footer_notes)
        ]
    ], colWidths=[42, 60, 42, 66, 42, 60])
    score_guide_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    r5_table = Table([[notes_content, score_guide_table]], colWidths=[240, 316])
    r5_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#E2E8F0")),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAFAFA")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(r5_table)
    story.append(Spacer(1, 4))

    # Bottom Black Disclaimer Bar
    disclaimer_p = Paragraph("THIS REPORT IS FOR REFERENCE ONLY AND DOES NOT DETERMINE PERSONAL WORTH.", footer_bar_txt)
    footer_bar = Table([[disclaimer_p]], colWidths=[556])
    footer_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#111111")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(footer_bar)

    # Build PDF
    doc.build(story)
    return pdf_path