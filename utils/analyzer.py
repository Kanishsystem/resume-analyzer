# def analyze_resume(text):
#     text_lower = text.lower()
#     score = 50 
#     improvements = []


#     keywords = ["python", "machine learning", "sql", "data analysis", "communication", "teamwork"]
#     matched = [kw for kw in keywords if kw in text_lower]
#     score += len(matched) * 2
  
    

#     if "skills" in text_lower:
#         score += 5
#     else:
#         improvements.append("Include a Skills section with relevant tools or technologies.")

#     if "education" in text_lower:
#         score += 5
#     else:
#         improvements.append("Include your Education details.")

#     if "experience" in text_lower:
#         score += 5
#     else:
#         improvements.append("Include your Work Experience section.")

#     if "project" in text_lower:
#         score += 5
#     else:
#         improvements.append("Add one or two key projects you've worked on.")

#     if len(text) < 300:
#         improvements.append("Your resume seems too short. Add more details about your experience or skills.")
#         score -= 10

#     score = max(0, min(score, 100))

#     return {
#         "score": score,
#         "improvements": improvements if improvements else ["Your resume looks great! Just ensure it’s well-formatted."]
#     }


from textblob import TextBlob
import re

def analyze_resume(text):
    text_lower = text.lower()
    results = []
    total_score = 0

    # --- Detect Stream / Department ---
    if re.search(r"b\.e|b\.tech|engineering|mechanical|computer|electrical", text_lower):
        stream = "ENGINEERING"
    elif re.search(r"b\.sc|m\.sc|physics|chemistry|mathematics|science", text_lower):
        stream = "SCIENCE"
    elif re.search(r"b\.com|m\.com|bba|mba|economics|management|commerce", text_lower):
        stream = "ARTS & MANAGEMENT"
    else:
        stream = "GENERAL"

    # --- Define benchmark (weighted parameters from your model.docx) ---
    benchmark = {
        "Technical Skills": 25,
        "Projects / Internships": 25,
        "Academic Performance": 10,
        "Certifications / Courses": 10,
        "Career Objective": 10,
        "Communication & Grammar": 10,
        "Formatting & Layout": 5,
        "Achievements / Awards": 5
    }

    # --- Define expected skills per stream ---
    skill_keywords = {
        "ENGINEERING": ["python", "matlab", "autocad", "solidworks", "c", "c++", "java", "embedded", "cad"],
        "SCIENCE": ["python", "research", "data analysis", "lab", "matlab", "statistics", "experiment"],
        "ARTS & MANAGEMENT": ["tally", "excel", "marketing", "finance", "communication", "leadership", "management"],
        "GENERAL": ["communication", "teamwork", "excel"]
    }

    # --- Evaluate each parameter ---
    for param, weight in benchmark.items():
        score = 0

        if param == "Technical Skills":
            matched = [kw for kw in skill_keywords[stream] if kw in text_lower]
            ratio = len(matched) / len(skill_keywords[stream])
            score = 100 * ratio if ratio > 0 else 40

        elif param == "Projects / Internships":
            score = 100 if re.search(r"project|intern", text_lower) else 50

        elif param == "Academic Performance":
            score = 80 if re.search(r"cgpa|percentage|grade|university|degree", text_lower) else 50

        elif param == "Certifications / Courses":
            score = 100 if re.search(r"coursera|nptel|certificate|certification|course", text_lower) else 40

        elif param == "Career Objective":
            score = 100 if re.search(r"objective|goal|career", text_lower) else 60

        elif param == "Communication & Grammar":
            blob = TextBlob(text)
            grammar_quality = 100 - (abs(blob.sentiment.subjectivity) * 100)
            score = grammar_quality

        elif param == "Formatting & Layout":
            score = 90 if len(text.split()) > 250 and re.search(r"skills|education|experience", text_lower) else 60

        elif param == "Achievements / Awards":
            score = 100 if re.search(r"award|achievement|winner|competition", text_lower) else 40

        weighted = score * (weight / 100)
        total_score += weighted

        results.append({
            "Parameter": param,
            "Weight": weight,
            "Score": round(score, 2),
            "Weighted": round(weighted, 2)
        })

    total = round(total_score, 2)

    # --- Suggestions ---
    suggestions = []
    if total < 60:
        suggestions.append("Add more technical and project details to improve your resume.")
    if "certificate" not in text_lower:
        suggestions.append("Include certifications or online courses.")
    if "objective" not in text_lower:
        suggestions.append("Add a clear career objective or summary.")
    if len(text) < 400:
        suggestions.append("Add more content to your resume.")

    if not suggestions:
        suggestions = ["Your resume aligns well with your stream benchmarks. Great job!"]

    return {
        "stream": stream,
        "total": total,
        "details": results,
        "suggestions": suggestions
    }

