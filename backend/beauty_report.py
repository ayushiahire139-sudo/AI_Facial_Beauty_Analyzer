def generate_beauty_report(
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
):

    report = {
        "overall_rating": "Excellent" if beauty_score >= 85 else "Good",

        "beauty_score": beauty_score,
        "symmetry_score": symmetry_score,
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

        "recommendation": "Maintain a healthy lifestyle and skincare routine."
    }

    return report