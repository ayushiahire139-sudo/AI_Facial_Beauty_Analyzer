def calculate_beauty_score(symmetry_score):
    """
    Calculates the overall beauty score based on facial symmetry.
    Returns a score between 0 and 100.
    """

    # Keep score within valid range
    if symmetry_score < 0:
        symmetry_score = 0

    if symmetry_score > 100:
        symmetry_score = 100

    beauty_score = round(symmetry_score, 2)

    return beauty_score