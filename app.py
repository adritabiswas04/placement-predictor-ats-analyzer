from flask import Flask, render_template, request
import pickle
import pandas as pd
import pdfplumber
from ats_analyzer import analyze_resume_ats

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))

# ------------------ SAFE FLOAT ------------------
def safe_float(val):
    try:
        return float(val)
    except:
        return 0


# ------------------ HOME ------------------
@app.route('/')
def home():
    return render_template("home.html")


# ------------------ PLACEMENT PAGE ------------------
@app.route('/placement')
def placement():
    return render_template("index.html")


# ------------------ PREDICTION ------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        cgpa = safe_float(request.form.get('cgpa'))
        internships = int(request.form.get('internships', 0))
        projects = int(request.form.get('projects', 0))
        skills = int(request.form.get('skills', 0))

        input_data = pd.DataFrame(
            [[cgpa, internships, projects, skills]],
            columns=["cgpa", "internships", "projects", "skills"]
        )

        prediction = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1] * 100
        prob = round(prob, 2)

        result = "Placed ✅" if prediction == 1 else "Not Placed ❌"

        return render_template("result.html", result=result, prob=prob)

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------ RESUME PAGE ------------------
@app.route('/resume')
def resume():
    return render_template("resume.html")


# ------------------ PDF EXTRACTION ------------------
def extract_text(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception as e:
        print("PDF Error:", e)

    return text.strip()


# ------------------ ATS ANALYSIS ------------------
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files['resume']
        jd_text = request.form['jd']

        resume_text = ""

        if file:
            resume_text = extract_text(file)

        # 🔥 DEBUG (VERY IMPORTANT)
        print("RESUME TEXT PREVIEW:", resume_text[:300])

        # ❌ If extraction failed
        if not resume_text:
            return render_template("resume_result.html", data={
                "ats_score": 0,
                "similarity": 0,
                "resume_skills": [],
                "missing_skills": [],
                "suggestions": ["⚠️ Could not read resume. Try another PDF."]
            })

        result = analyze_resume_ats(resume_text, jd_text)

        return render_template("resume_result.html", data=result)

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)