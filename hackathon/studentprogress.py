from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Expanded Question Bank
question_bank = [
    # Math - Beginner
    {"subject": "Math", "difficulty": "Beginner", "text": "What is 2 + 2?", "answer": "4"},
    {"subject": "Math", "difficulty": "Beginner", "text": "What is 5 - 3?", "answer": "2"},
    {"subject": "Math", "difficulty": "Beginner", "text": "What is 10 ÷ 2?", "answer": "5"},
    {"subject": "Math", "difficulty": "Beginner", "text": "What is 7 + 6?", "answer": "13"},

    # Math - Intermediate
    {"subject": "Math", "difficulty": "Intermediate", "text": "Solve: 12 * 8", "answer": "96"},
    {"subject": "Math", "difficulty": "Intermediate", "text": "What is the square root of 144?", "answer": "12"},
    {"subject": "Math", "difficulty": "Intermediate", "text": "Solve: (15 * 3) - 10", "answer": "35"},
    {"subject": "Math", "difficulty": "Intermediate", "text": "What is 25% of 200?", "answer": "50"},

    # Math - Advanced
    {"subject": "Math", "difficulty": "Advanced", "text": "Integrate x^2 dx", "answer": "x^3/3 + c"},
    {"subject": "Math", "difficulty": "Advanced", "text": "Differentiate sin(x)", "answer": "cos(x)"},
    {"subject": "Math", "difficulty": "Advanced", "text": "Solve: Limit of (1 + 1/n)^n as n→∞", "answer": "e"},
    {"subject": "Math", "difficulty": "Advanced", "text": "Find derivative of ln(x)", "answer": "1/x"},

    # Science - Beginner
    {"subject": "Science", "difficulty": "Beginner", "text": "What planet is known as the Red Planet?", "answer": "mars"},
    {"subject": "Science", "difficulty": "Beginner", "text": "What gas do humans need to breathe?", "answer": "oxygen"},
    {"subject": "Science", "difficulty": "Beginner", "text": "What is the freezing point of water (°C)?", "answer": "0"},
    {"subject": "Science", "difficulty": "Beginner", "text": "What star gives Earth light and heat?", "answer": "sun"},

    # Science - Intermediate
    {"subject": "Science", "difficulty": "Intermediate", "text": "What is H2O commonly known as?", "answer": "water"},
    {"subject": "Science", "difficulty": "Intermediate", "text": "Which gas do plants release during photosynthesis?", "answer": "oxygen"},
    {"subject": "Science", "difficulty": "Intermediate", "text": "What is the chemical symbol for Gold?", "answer": "au"},
    {"subject": "Science", "difficulty": "Intermediate", "text": "What is the speed of light in vacuum (approx km/s)?", "answer": "300000"},

    # Science - Advanced
    {"subject": "Science", "difficulty": "Advanced", "text": "Explain Newton's third law of motion.", "answer": "every action has equal and opposite reaction"},
    {"subject": "Science", "difficulty": "Advanced", "text": "What is the chemical formula of methane?", "answer": "ch4"},
    {"subject": "Science", "difficulty": "Advanced", "text": "What particle carries a negative charge?", "answer": "electron"},
    {"subject": "Science", "difficulty": "Advanced", "text": "Define entropy in thermodynamics.", "answer": "measure of disorder"},
]

# Student profile
student_profile = {
    "name": "Boobalan",
    "level": "Beginner",  # Initial level
    "score": 0
}

# Allocate questions according to level
def allocate_questions(profile, bank, num_questions=5):
    questions = [q for q in bank if q["difficulty"] == profile["level"]]
    return random.sample(questions, min(len(questions), num_questions))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answers = request.form.to_dict()
        allocated_questions = session.get("allocated_questions", [])

        correct = 0
        total = len(allocated_questions)

        for i, q in enumerate(allocated_questions):
            student_answer = answers.get(f"q_{i}", "").strip().lower()
            correct_answer = q["answer"].lower()
            if student_answer == correct_answer:
                correct += 1

        # Update score
        student_profile["score"] += correct

        # Accuracy check
        accuracy = (correct / total) * 100 if total > 0 else 0

        # Adjust learning level
        if accuracy > 70 and student_profile["level"] == "Beginner":
            student_profile["level"] = "Intermediate"
        elif accuracy > 70 and student_profile["level"] == "Intermediate":
            student_profile["level"] = "Advanced"
        elif accuracy < 40 and student_profile["level"] == "Advanced":
            student_profile["level"] = "Intermediate"
        elif accuracy < 40 and student_profile["level"] == "Intermediate":
            student_profile["level"] = "Beginner"

        return redirect(url_for("index"))

    # Allocate new set of questions
    allocated_questions = allocate_questions(student_profile, question_bank)
    session["allocated_questions"] = allocated_questions

    return render_template("index.html", profile=student_profile, questions=allocated_questions)


if __name__ == "__main__":
    app.run(debug=True)
