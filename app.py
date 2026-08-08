from flask import Flask, render_template, request

app = Flask(__name__)

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
    name = request.form.get("name")
    email = request.form.get("email")

    return render_question(
        name,
        email,
        0
    )


@app.route("/question/<int:number>", methods=["POST"])
def next_question(number):
    name = request.form.get("name")
    email = request.form.get("email")

    return render_question(
        name,
        email,
        number
    )


def render_question(name, email, index):

    if index >= len(questions):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AB InterVue AI - Complete</title>
        </head>

        <body style="text-align:center; font-family:Arial; margin-top:100px;">

            <h1>Interview Completed!</h1>

            <p>Great job, {name}!</p>

            <p>
                You have successfully completed the interview.
            </p>

            <button onclick="window.location.href='/'">
                Start New Interview
            </button>

        </body>
        </html>
        """

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

            <input
                type="hidden"
                name="name"
                value="{name}"
            >

            <input
                type="hidden"
                name="email"
                value="{email}"
            >

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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
