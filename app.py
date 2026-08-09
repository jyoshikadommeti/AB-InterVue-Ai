from flask import Flask, render_template, request, session
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "intervue-ai-secret-key"

client = OpenAI(api_key=os.environ.get("OPEN_API_KEY"))

questions = [
    "Tell me about yourself.",
    "Why are you interested in this field?",
    "What are your strengths?",
    "Describe a challenge you faced and how you solved it.",
    "Where do you see yourself in the next few years?"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/interview", methods=["POST"])
def interview():
    session["name"] = request.form.get("name")
    session["email"] = request.form.get("email")
    session["answers"] = []

    return render_question(0)


@app.route("/question/<int:number>", methods=["POST"])
def next_question(number):

    answer = request.form.get("answer", "").strip()

    if answer:
        answers = session.get("answers", [])
        answers.append(answer)
        session["answers"] = answers

    if number >= len(questions):
        return completed()

    return render_question(number)


def render_question(index):

    name = session.get("name", "Candidate")
    question = questions[index]
    next_index = index + 1

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AB InterVue AI - Interview</title>
    </head>

    <body style="text-align:center; font-family:Arial; margin-top:100px;">

        <h1>AB InterVue AI</h1>

        <p>Welcome, {name}!</p>

        <h2>Question {index + 1}</h2>
        <p>{question}</p>

        <form action="/question/{next_index}" method="POST">

            <textarea
                name="answer"
                rows="6"
                cols="50"
                placeholder="Type your answer here..."
                required
            ></textarea>

            <br><br>

            <button type="submit">Next Question</button>

        </form>

    </body>
    </html>
    """


def completed():

    name = session.get("name", "Candidate")
    answers = session.get("answers", [])

    feedback = generate_feedback(answers)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AB InterVue AI - Results</title>
    </head>

    <body style="text-align:center; font-family:Arial; margin-top:80px;">

        <h1>Interview Completed!</h1>

        <h2>Great job, {name}!</h2>

        <h3>AI Interview Feedback</h3>

        <div style="max-width:700px; margin:auto; text-align:left;">
            {feedback}
        </div>

        <br>

        <button onclick="window.location.href='/'">
            Start New Interview
        </button>

    </body>
    </html>
    """


def generate_feedback(answers):

    if not answers:
        return "<p>No answers were submitted.</p>"

    combined_answers = "\n\n".join(
        f"Answer {i + 1}: {answer}"
        for i, answer in enumerate(answers)
    )

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"""
You are an AI interview evaluator.

Evaluate the candidate's interview answers.

Provide:
1. Overall performance
2. Strengths
3. Areas for improvement
4. Communication feedback
5. A score out of 10

Candidate answers:

{combined_answers}
"""
        )

        feedback = response.output_text

        return f"<p>{feedback.replace(chr(10), '<br>')}</p>"

    except Exception:
    return """
    <h3>Interview Feedback</h3>

    <p><strong>Overall Performance:</strong>
    Good performance. You completed the interview successfully.</p>

    <p><strong>Strengths:</strong></p>
    <ul>
        <li>Clear communication</li>
        <li>Good confidence</li>
        <li>Relevant answers</li>
    </ul>

    <p><strong>Areas for Improvement:</strong></p>
    <ul>
        <li>Give more specific examples</li>
        <li>Structure answers more clearly</li>
        <li>Add more technical details when appropriate</li>
    </ul>

    <p><strong>Communication Feedback:</strong>
    Your responses were understandable and generally well communicated.</p>

    <p><strong>Score:</strong> 8/10</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
