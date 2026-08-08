from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "intervue-ai-secret-key"

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
        session["answers"].append(answer)

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

            <button type="submit">
                Next Question
            </button>

        </form>

    </body>
    </html>
    """


def completed():

    name = session.get("name", "Candidate")
    answers = session.get("answers", [])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AB InterVue AI - Complete</title>
    </head>

    <body style="text-align:center; font-family:Arial; margin-top:100px;">

        <h1>Interview Completed!</h1>

        <p>Great job, {name}!</p>

        <p>Your {len(answers)} answers have been recorded.</p>

        <button onclick="window.location.href='/'">
            Start New Interview
        </button>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "intervue-ai-secret-key"

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
        session["answers"].append(answer)

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

            <button type="submit">
                Next Question
            </button>

        </form>

    </body>
    </html>
    """


def completed():

    name = session.get("name", "Candidate")
    answers = session.get("answers", [])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AB InterVue AI - Complete</title>
    </head>

    <body style="text-align:center; font-family:Arial; margin-top:100px;">

        <h1>Interview Completed!</h1>

        <p>Great job, {name}!</p>

        <p>Your {len(answers)} answers have been recorded.</p>

        <button onclick="window.location.href='/'">
            Start New Interview
        </button>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
