from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Question bank
question_bank = [
    {"subject": "Math", "difficulty": "Beginner", "text": "What is 2 + 2?", "answer": "4"},
    {"subject": "Math", "difficulty": "Intermediate", "text": "Solve: 12 * 8", "answer": "96"},
    {"subject": "Math", "difficulty": "Advanced", "text": "Integrate x^2 dx", "answer": "x^3/3 + C"},
    {"subject": "Science", "difficulty": "Beginner", "text": "What planet is known as the Red Planet?", "answer": "Mars"},
    {"subject": "Science", "difficulty": "Intermediate", "text": "What is H2O commonly known as?", "answer": "Water"},
    {"subject": "Science", "difficulty": "Advanced", "text": "Explain Newton's third law of motion.", "answer": "For every action, there is an equal and opposite reaction"},
    {"subject": "Math", "difficulty": "Beginner", "text": "What is 5 - 3?", "answer": "2"},
    {"subject": "Science", "difficulty": "Beginner", "text": "Which gas do we breathe in to live?", "answer": "Oxygen"}
]

# Allocate non-repeating questions
def allocate_questions(profile, bank, num_questions=5):
    pool = [q for q in bank if q["subject"] in (profile["preferred_subjects"] + profile["weak_areas"])
            and q["difficulty"] == profile["level"]]
    num_questions = min(num_questions, len(pool))
    allocated = random.sample(pool, num_questions)  # no repeats
    return allocated

# Home page: student input
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        level = request.form.get("level")
        subjects = request.form.getlist("subjects") or ["Math", "Science"]

        student_profile = {
            "name": name,
            "level": level,
            "preferred_subjects": subjects,
            "weak_areas": ["Science"]
        }

        questions = allocate_questions(student_profile, question_bank)

        return render_template("assessment.html", profile=student_profile, questions=questions)
    
    return render_template("index.html")

# Handle quiz submission
@app.route("/submit", methods=["POST"])
def submit():
    total_questions = int(request.form.get("total_questions"))
    score = 0
    answers = []

    for i in range(total_questions):
        q_text = request.form.get(f"q_text_{i}")
        q_subject = request.form.get(f"q_subject_{i}")
        q_difficulty = request.form.get(f"q_difficulty_{i}")
        q_answer = request.form.get(f"q_answer_{i}")
        user_answer = request.form.get(f"user_answer_{i}")

        if user_answer.strip().lower() == q_answer.strip().lower():
            score += 1

        answers.append({
            "text": q_text,
            "subject": q_subject,
            "difficulty": q_difficulty,
            "correct": q_answer,
            "user": user_answer
        })

    return render_template("result.html", score=score, total=total_questions, answers=answers)

if __name__ == "__main__":
    app.run(debug=True)
