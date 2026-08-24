from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf_report(report_data, filename):

    reports_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "reports"
    )

    os.makedirs(reports_folder, exist_ok=True)

    pdf_path = os.path.join(reports_folder, filename)

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph("<b><font size=20>AI Facial Beauty Analyzer Report</font></b>", styles["Title"])
    )

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    # Overall Rating
    story.append(
        Paragraph("<b>Overall Rating</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(report_data["overall_rating"], styles["BodyText"])
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    # Scores
    story.append(Paragraph("<b>Scores</b>", styles["Heading2"]))

    story.append(
        Paragraph(f"Beauty Score : {report_data['beauty_score']}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Symmetry Score : {report_data['symmetry_score']}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Golden Ratio Score : {report_data['golden_ratio_score']}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Face Shape : {report_data['face_shape']}", styles["BodyText"])
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    # Eye Analysis
    story.append(Paragraph("<b>Eye Analysis</b>", styles["Heading2"]))

    eye = report_data["eye_analysis"]

    story.append(Paragraph(f"Eye Distance : {eye['eye_distance']}", styles["BodyText"]))
    story.append(Paragraph(f"Eye Size : {eye['eye_size']}", styles["BodyText"]))
    story.append(Paragraph(f"Eye Symmetry : {eye['eye_symmetry']}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    # Nose Analysis
    story.append(Paragraph("<b>Nose Analysis</b>", styles["Heading2"]))

    nose = report_data["nose_analysis"]

    story.append(Paragraph(f"Nose Width : {nose['nose_width']}", styles["BodyText"]))
    story.append(Paragraph(f"Nose Length : {nose['nose_length']}", styles["BodyText"]))
    story.append(Paragraph(f"Nose Shape : {nose['nose_shape']}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    # Lip Analysis
    story.append(Paragraph("<b>Lip Analysis</b>", styles["Heading2"]))

    lip = report_data["lip_analysis"]

    story.append(Paragraph(f"Lip Width : {lip['lip_width']}", styles["BodyText"]))
    story.append(Paragraph(f"Lip Height : {lip['lip_height']}", styles["BodyText"]))
    story.append(Paragraph(f"Lip Shape : {lip['lip_shape']}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    # Jaw Analysis
    story.append(Paragraph("<b>Jaw Analysis</b>", styles["Heading2"]))

    jaw = report_data["jaw_analysis"]

    story.append(Paragraph(f"Jaw Width : {jaw['jaw_width']}", styles["BodyText"]))
    story.append(Paragraph(f"Jaw Shape : {jaw['jaw_shape']}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    # Personal Details
    story.append(Paragraph("<b>Personal Details</b>", styles["Heading2"]))

    story.append(Paragraph(f"Skin Tone : {report_data['skin_tone']}", styles["BodyText"]))
    story.append(Paragraph(f"Estimated Age : {report_data['estimated_age']}", styles["BodyText"]))
    story.append(Paragraph(f"Gender : {report_data['gender']}", styles["BodyText"]))
    story.append(Paragraph(f"Emotion : {report_data['emotion']}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    # Recommendation
    story.append(Paragraph("<b>Recommendation</b>", styles["Heading2"]))

    story.append(
        Paragraph(report_data["recommendation"], styles["BodyText"])
    )

    doc.build(story)

    return pdf_path