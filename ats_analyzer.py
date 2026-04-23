import re

# ------------------ TEXT CLEANING ------------------
def extract_words(text):
    text = text.lower()
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return set(words)


# ------------------ MAIN FUNCTION ------------------
def analyze_resume_ats(resume_text, jd_text):

    # Extract words
    resume_words = extract_words(resume_text)
    jd_words = extract_words(jd_text)

    # ------------------ SYNONYMS ------------------
    synonyms = {
        "ml": ["machine", "learning"],
        "ai": ["artificial", "intelligence"],
        "js": ["javascript"],
        "ds": ["data", "structures"],
        "db": ["database", "sql"]
    }

    # Apply synonyms to resume
    for word in list(resume_words):
        if word in synonyms:
            resume_words.update(synonyms[word])

    # Apply synonyms to JD
    for word in list(jd_words):
        if word in synonyms:
            jd_words.update(synonyms[word])

    # ------------------ MATCHING ------------------
    matched = resume_words.intersection(jd_words)

    # Similarity score
    if len(jd_words) == 0:
        similarity = 0
    else:
        similarity = (len(matched) / len(jd_words)) * 100

    # ------------------ SKILLS LIST ------------------
    skills_list = [
        "python", "java", "c", "c++", "sql",
        "html", "css", "javascript", "react", "flask",
        "machine", "learning", "nlp",
        "data", "structures", "algorithms"
    ]

    # Resume skills
    resume_skills = [skill for skill in skills_list if skill in resume_words]

    # Missing skills (only if present in JD but not in resume)
    missing_skills = [
        skill for skill in skills_list
        if skill in jd_words and skill not in resume_words
    ]

    # ------------------ ATS SCORE ------------------
    ats_score = (len(resume_skills) / len(skills_list)) * 100

    # ------------------ SUGGESTIONS ------------------
    suggestions = []

    if similarity < 50:
        suggestions.append("Increase keyword match with job description")

    if missing_skills:
        suggestions.append("Add missing technical skills")

    if len(resume_words) < 100:
        suggestions.append("Improve resume content alignment with JD")

    if ats_score > 75:
        suggestions.append("Great! Your resume is well optimized 🎯")

    # ------------------ RETURN ------------------
    return {
        "ats_score": round(ats_score, 2),
        "similarity": round(similarity, 2),
        "resume_skills": resume_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }