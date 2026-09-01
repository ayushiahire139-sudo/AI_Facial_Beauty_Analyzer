from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from PIL import Image as PILImage
import os
from datetime import datetime

def get_scaled_reportlab_image(image_path, max_width=215, max_height=175):
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
        print(f"Error loading image '{image_path}' for PDF report: {e}")
        return None

def generate_pdf_report(report_data, filename, original_image_path=None, landmarks_image_path=None):
    reports_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "reports"
    )
    os.makedirs(reports_folder, exist_ok=True)
    pdf_path = os.path.join(reports_folder, filename)

    # Document Setup (0.75-inch margins)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#4C1D95")    # Deep Aubergine
    c_secondary = colors.HexColor("#8B5CF6")  # Lavender Purple
    c_dark = colors.HexColor("#1E1B4B")       # Dark Charcoal
    c_light = colors.HexColor("#F5F3FF")      # Light Tint
    c_border = colors.HexColor("#E2E8F0")     # Light Border Gray

    # Custom Paragraph Styles
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.white
    )
    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#DDD6FE")
    )
    style_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceAfter=8,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark
    )
    style_body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=style_body,
        fontName='Helvetica-Bold'
    )
    style_cell_header = ParagraphStyle(
        'CellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        textColor=colors.white
    )
    style_cell_body = ParagraphStyle(
        'CellBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_dark
    )
    style_metric_title = ParagraphStyle(
        'MetricTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        textColor=c_secondary,
        alignment=1 # Center
    )
    style_metric_value = ParagraphStyle(
        'MetricValue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=1 # Center
    )
    style_img_caption = ParagraphStyle(
        'ImgCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_primary,
        alignment=1 # Center
    )

    story = []

    # ==========================================
    # 1. HEADER BAND
    # ==========================================
    title_text = "<b>AI FACIAL ANALYSIS REPORT</b>"
    date_str = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    subtitle_text = f"Proportions, Harmony and Skincare Guidelines  |  Generated {date_str}"
    
    header_data = [
        [Paragraph(title_text, style_title)],
        [Paragraph(subtitle_text, style_subtitle)]
    ]
    header_table = Table(header_data, colWidths=[504])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_primary),
        ('PADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,1), (-1,1), 14),
        ('TOPPADDING', (0,0), (-1,0), 14),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))

    # ==========================================
    # 2. OVERALL STATS SECTION (Grid Cards Layout)
    # ==========================================
    metrics_data = [
        [
            Paragraph("BEAUTY HARMONY", style_metric_title),
            Paragraph("SYMMETRY SCORE", style_metric_title),
            Paragraph("GOLDEN RATIO", style_metric_title),
            Paragraph("FACE SHAPE", style_metric_title)
        ],
        [
            Paragraph(f"{report_data['beauty_score']}/100", style_metric_value),
            Paragraph(f"{report_data['symmetry_score']}/100", style_metric_value),
            Paragraph(f"{report_data['golden_ratio_score']}/100", style_metric_value),
            Paragraph(str(report_data['face_shape']), style_metric_value)
        ]
    ]
    metrics_table = Table(metrics_data, colWidths=[126, 126, 126, 126])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_secondary),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 3),
        ('TOPPADDING', (0,1), (-1,1), 3),
        ('BOTTOMPADDING', (0,1), (-1,1), 10),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 14))

    # ==========================================
    # 3. VISUAL FACE MAPPING & LANDMARK ALIGNMENT
    # ==========================================
    orig_path = original_image_path or report_data.get("original_image_path")
    mesh_path = landmarks_image_path or report_data.get("landmarks_image_path")

    orig_rl_img = get_scaled_reportlab_image(orig_path, max_width=215, max_height=170)
    mesh_rl_img = get_scaled_reportlab_image(mesh_path, max_width=215, max_height=170)

    if orig_rl_img or mesh_rl_img:
        story.append(Paragraph("Visual Face Mapping &amp; Landmark Alignment", style_heading))
        
        col1 = [
            Paragraph("ORIGINAL PORTRAIT", style_img_caption),
            Spacer(1, 5),
            orig_rl_img if orig_rl_img else Paragraph("Image Not Available", style_body)
        ]
        
        col2 = [
            Paragraph("3D LANDMARK MESH (468 POINTS)", style_img_caption),
            Spacer(1, 5),
            mesh_rl_img if mesh_rl_img else Paragraph("Landmarks Not Available", style_body)
        ]

        mapping_table = Table([[col1, col2]], colWidths=[246, 246])
        mapping_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_light),
            ('BOX', (0,0), (-1,-1), 1, c_secondary),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(mapping_table)
        story.append(Spacer(1, 14))

    # ==========================================
    # 4. PROFILE SUMMARY BLOCK
    # ==========================================
    summary_data = [
        [Paragraph("<b>ESTIMATED AGE:</b>", style_body), Paragraph(str(report_data['estimated_age']), style_body),
         Paragraph("<b>SKIN TONE:</b>", style_body), Paragraph(str(report_data['skin_tone']), style_body)],
        [Paragraph("<b>GENDER:</b>", style_body), Paragraph(str(report_data['gender']), style_body),
         Paragraph("<b>EMOTION:</b>", style_body), Paragraph(str(report_data['emotion']), style_body)]
    ]
    summary_table = Table(summary_data, colWidths=[110, 142, 90, 162])
    summary_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # ==========================================
    # 5. DETAILED FEATURE RATIOS TABLE
    # ==========================================
    story.append(Paragraph("Facial Feature Metric Analysis", style_heading))
    
    eye = report_data["eye_analysis"]
    nose = report_data["nose_analysis"]
    lip = report_data["lip_analysis"]
    jaw = report_data["jaw_analysis"]

    table_data = [
        [
            Paragraph("Facial Feature", style_cell_header), 
            Paragraph("Analysis Category", style_cell_header), 
            Paragraph("Proportional Assessment", style_cell_header)
        ],
        [
            Paragraph("<b>Eyes</b>", style_body), 
            Paragraph(f"Distance: {eye['eye_distance']}", style_cell_body), 
            Paragraph(f"Size: {eye['eye_size']} | Symmetry: {eye['eye_symmetry']}", style_cell_body)
        ],
        [
            Paragraph("<b>Nose</b>", style_body), 
            Paragraph(f"Width: {nose['nose_width']}", style_cell_body), 
            Paragraph(f"Length: {nose['nose_length']} | Shape: {nose['nose_shape']}", style_cell_body)
        ],
        [
            Paragraph("<b>Lips</b>", style_body), 
            Paragraph(f"Width: {lip['lip_width']}", style_cell_body), 
            Paragraph(f"Height: {lip['lip_height']} | Shape: {lip['lip_shape']}", style_cell_body)
        ],
        [
            Paragraph("<b>Jaw / Contour</b>", style_body), 
            Paragraph(f"Width: {jaw['jaw_width']}", style_cell_body), 
            Paragraph(f"Shape: {jaw['jaw_shape']}", style_cell_body)
        ]
    ]
    
    ratios_table = Table(table_data, colWidths=[120, 160, 224])
    ratios_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(ratios_table)
    story.append(Spacer(1, 16))

    # ==========================================
    # 6. PERSONALIZED AI RECOMMENDATIONS
    # ==========================================
    story.append(Paragraph("AI Recommendations & Guidelines", style_heading))
    
    recs = report_data.get("recommendations", {})
    
    rec_skincare = recs.get("skincare", "Maintain your daily hydration and sunscreen routine.")
    rec_hair = recs.get("hairstyle", "Select styles that fit your facial profile.")
    rec_makeup = recs.get("makeup", "Apply natural shades aligned with your skin tone brightness.")
    rec_lifestyle = recs.get("lifestyle", "Practice wellness, diet guidelines, and sound sleep.")

    rec_data = [
        [Paragraph("<b>🧴 Skincare &amp; Protection:</b>", style_body_bold)],
        [Paragraph(rec_skincare, style_body)],
        [Spacer(1, 4)],
        [Paragraph("<b>💇 Hairstyle &amp; Profile:</b>", style_body_bold)],
        [Paragraph(rec_hair, style_body)],
        [Spacer(1, 4)],
        [Paragraph("<b>💄 Cosmetics &amp; Accentuation:</b>", style_body_bold)],
        [Paragraph(rec_makeup, style_body)],
        [Spacer(1, 4)],
        [Paragraph("<b>🥗 Wellness &amp; Lifestyle:</b>", style_body_bold)],
        [Paragraph(rec_lifestyle, style_body)]
    ]
    
    rec_table = Table(rec_data, colWidths=[504])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('PADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 16))

    # ==========================================
    # 7. DISCLAIMER FOOTER
    # ==========================================
    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#94A3B8"),
        alignment=1 # Center
    )
    disclaimer_text = (
        "Disclaimer: This report is generated automatically using artificial intelligence models. "
        "It evaluates superficial geometric proportions and is intended for personal styling, grooming "
        "inspiration, and entertainment purposes only. It does not constitute medical, health, or clinical skin advice."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(story)
    return pdf_path