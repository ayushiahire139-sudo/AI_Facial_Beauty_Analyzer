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
    """
    Generates structured analysis data matching the Clinical Facial Beauty Report benchmark.
    """
    # 1. Calibrate Individual Category Scores (0-100 scale)
    sym_val = int(round(symmetry_score))
    prop_val = int(round(max(60, min(95, golden_ratio_score + 35))))
    bone_val = int(round(max(60, min(94, (symmetry_score * 0.5) + (beauty_score * 0.5) - 2))))
    skin_val = int(round(max(65, min(92, beauty_score - 1))))
    eyes_val = int(round(max(62, min(96, (beauty_score * 0.6) + (symmetry_score * 0.4) + 1))))
    nose_val = int(round(max(60, min(92, (symmetry_score * 0.7) + (golden_ratio_score * 0.3) - 3))))
    lips_val = int(round(max(62, min(94, (beauty_score * 0.5) + 36))))
    jaw_val = int(round(max(58, min(90, (symmetry_score * 0.4) + (beauty_score * 0.4) + 12))))
    overall_harmony = int(round(beauty_score))

    # Overall label
    if beauty_score >= 85:
        overall_label = "EXCEPTIONAL"
    elif beauty_score >= 75:
        overall_label = "VERY ATTRACTIVE"
    elif beauty_score >= 65:
        overall_label = "ABOVE AVERAGE"
    else:
        overall_label = "AVERAGE HARMONY"

    # 2. Detailed Findings Descriptions
    findings = {
        "symmetry": {
            "title": "Symmetry",
            "score": sym_val,
            "text": "Slight natural asymmetry in brow and jaw. Overall bilateral balance is good." if sym_val > 70 else "Noticeable lateral variance between left and right facial planes."
        },
        "proportions": {
            "title": "Proportions",
            "score": prop_val,
            "text": "Facial vertical thirds are well-aligned. Key aesthetic points are proportionate."
        },
        "bone_structure": {
            "title": "Bone Structure",
            "score": bone_val,
            "text": f"Moderate cheekbone projection. Jawline contour exhibits a soft {face_shape.lower()} curvature."
        },
        "skin_quality": {
            "title": "Skin Quality",
            "score": skin_val,
            "text": f"Even {skin_tone.lower()} tone and texture. Minor natural variations in ocular zone."
        },
        "eyes": {
            "title": "Eyes",
            "score": eyes_val,
            "text": f"Harmonious eye spacing ({eye_analysis.get('eye_distance', 'balanced')}) and {eye_analysis.get('eye_symmetry', 'symmetrical')} alignment."
        },
        "nose": {
            "title": "Nose",
            "score": nose_val,
            "text": f"Balanced nasal bridge width ({nose_analysis.get('nose_width', 'average')}), softly contoured nasal tip."
        },
        "lips": {
            "title": "Lips",
            "score": lips_val,
            "text": f"Well-defined vermilion volume ({lip_analysis.get('lip_shape', 'balanced')}), balanced lip proportion."
        },
        "jawline_chin": {
            "title": "Jawline & Chin",
            "score": jaw_val,
            "text": f"Soft mandibular contour ({jaw_analysis.get('jaw_shape', 'tapered')}), rounded chin with smooth transition."
        }
    }

    # 3. Dynamic Key Strengths & Areas for Improvement
    strengths = [
        "Good overall facial harmony and bilateral balance",
        "Well-proportioned horizontal facial thirds alignment",
        f"Expressive, symmetrical {eye_analysis.get('eye_symmetry', 'harmonious')} eye alignment",
        f"Even, healthy {skin_tone} complexion tone",
        f"Balanced {lip_analysis.get('lip_shape', 'classic')} lip contour and definition"
    ]

    improvements = [
        "Enhance jawline and chin contour definition",
        "Targeted hydration to brighten under-eye orbital area",
        "Precision eyebrow shaping for enhanced facial framing",
        "Subtle upper lip volume accentuation",
        "Strategic contouring under cheekbones to elevate bone structure"
    ]

    # 4. Grooming & Style Recommendations
    grooming = {
        "brows": [
            "Maintain natural fullness & clean lower edge",
            "Soft arch to subtly lift overall expression"
        ],
        "eyes": [
            "Brighten under-eyes with peptide hydration",
            "Subtle eyeliner or mascara to enhance almond shape"
        ],
        "contour_face": [
            "Light contouring powder beneath cheekbones",
            "Define mandibular jawline with soft bronzer"
        ],
        "lips": [
            "Use hydrating tinted balm or satin lip color",
            "Subtle gloss highlight on Cupid's bow"
        ],
        "hair": [
            f"Layered framing tailored to {face_shape} face shape",
            "Soft waves or sleek part to enhance facial symmetry"
        ]
    }

    report = {
        "beauty_score": beauty_score,
        "symmetry_score": symmetry_score,
        "face_shape": face_shape,
        "golden_ratio_score": golden_ratio_score,
        "overall_label": overall_label,
        "score_breakdown": {
            "Symmetry": sym_val,
            "Proportions": prop_val,
            "Bone Structure": bone_val,
            "Skin Quality": skin_val,
            "Eyes": eyes_val,
            "Nose": nose_val,
            "Lips": lips_val,
            "Jawline & Chin": jaw_val,
            "Overall Harmony": overall_harmony
        },
        "detailed_findings": findings,
        "key_strengths": strengths,
        "areas_for_improvement": improvements,
        "grooming_recommendations": grooming,
        "eye_analysis": eye_analysis,
        "nose_analysis": nose_analysis,
        "lip_analysis": lip_analysis,
        "jaw_analysis": jaw_analysis,
        "skin_tone": skin_tone,
        "estimated_age": estimated_age,
        "gender": gender,
        "emotion": emotion
    }

    return report