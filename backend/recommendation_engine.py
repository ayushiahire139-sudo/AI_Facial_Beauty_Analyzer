def generate_recommendations(
    beauty_score,
    face_shape,
    eye_analysis,
    nose_analysis,
    lip_analysis,
    jaw_analysis,
    skin_tone,
    emotion
):

    recommendations = {
        "skincare": "",
        "hairstyle": "",
        "makeup": "",
        "lifestyle": "",
        "confidence": ""
    }

  
    # ----------------------------
    # Beauty Score
    # ----------------------------
    if beauty_score >= 85:
        recommendations["confidence"] = (
            "Excellent facial harmony. Maintain your current skincare routine."
        )
    elif beauty_score >= 70:
        recommendations["confidence"] = (
            "Good facial balance. Small improvements can enhance your appearance."
        )
    else:
        recommendations["confidence"] = (
            "Focus on skincare, grooming, and a healthy lifestyle."
        )

    # ----------------------------
    # Face Shape
    # ----------------------------
    if face_shape == "Round":
        recommendations["hairstyle"] = (
            "Layered haircut or long hairstyle suits round faces."
        )

    elif face_shape == "Oval":
        recommendations["hairstyle"] = (
            "Most hairstyles suit an oval face."
        )

    elif face_shape == "Square":
        recommendations["hairstyle"] = (
            "Soft layered hairstyles help balance square faces."
        )

    else:
        recommendations["hairstyle"] = (
            "Choose hairstyles according to your face shape."
        )

    # ----------------------------
    # Skin Tone
    # ----------------------------
    if skin_tone == "Fair":
        recommendations["skincare"] = (
            "Use sunscreen SPF 50 and moisturizer daily."
        )

    elif skin_tone == "Medium":
        recommendations["skincare"] = (
            "Use Vitamin C serum, sunscreen, and moisturizer."
        )

    else:
        recommendations["skincare"] = (
            "Use hydrating moisturizer and sunscreen regularly."
        )

    # ----------------------------
    # Emotion
    # ----------------------------
    if emotion == "Serious":
        recommendations["lifestyle"] = (
            "Smile more often and practice stress management."
        )

    elif emotion == "Happy":
        recommendations["lifestyle"] = (
            "Maintain your positive lifestyle and healthy habits."
        )

    else:
        recommendations["lifestyle"] = (
            "Maintain a healthy daily routine."
        )

    # ----------------------------
    # Makeup
    # ----------------------------
    recommendations["makeup"] = (
        "Choose natural makeup shades that match your skin tone."
    )

    return recommendations
