def analyze_resume(text):
    text_lower = text.lower()
    score = 50  # base score
    improvements = []

    # Check for important keywords
    keywords = ["python", "machine learning", "sql", "data analysis", "communication", "teamwork"]
    matched = [kw for kw in keywords if kw in text_lower]
    score += len(matched) * 2
  

    

    # if "objective" not in text_lower:
    #     improvements.append("Add a professional objective or summary section.")
    # if "education" not in text_lower:
    #     improvements.append("Include your Education details.")
    # if "experience" not in text_lower:
    #     improvements.append("Include your Work Experience section.")
    # if "skills" not in text_lower:
    #     improvements.append("Include a Skills section with relevant tools or technologies.")
    # if "project" not in text_lower:
    #     improvements.append("Add one or two key projects you've worked on.")

     # Section detection
    if "skills" in text_lower:
        score += 5
    else:
        improvements.append("Include a Skills section with relevant tools or technologies.")

    if "education" in text_lower:
        score += 5
    else:
        improvements.append("Include your Education details.")

    if "experience" in text_lower:
        score += 5
    else:
        improvements.append("Include your Work Experience section.")

    if "project" in text_lower:
        score += 5
    else:
        improvements.append("Add one or two key projects you've worked on.")

    if len(text) < 300:
        improvements.append("Your resume seems too short. Add more details about your experience or skills.")
        score -= 10

    # Ensure score within 0–100
    score = max(0, min(score, 100))

    return {
        "score": score,
        "improvements": improvements if improvements else ["Your resume looks great! Just ensure it’s well-formatted."]
    }
