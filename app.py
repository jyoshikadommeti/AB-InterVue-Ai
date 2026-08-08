from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/interview", methods=["POST"])
def interview():
    name = request.form.get("name")
    email = request.form.get("email")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AB InterVue AI - Interview</title>
    </head>

    <body style="text-align:center; font-family:Arial; margin-top:100px;">

        <h1>Welcome, {name}!</h1>
        <p>Your interview is ready to begin.</p>

        <h2>Question 1</h2>
        <p>Tell me about yourself.</p>

        <form action="/question2" method="POST">
            <input type="hidden" name="name" value="{name}">
            <input type="hidden" name="email" value="{email}">

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


@app.route("/question2", methods=["POST"])
def question2():
    name = request.form.get("name")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AB InterVue AI - Interview</title>
    </head>

    <body style="text-align:center; font-family:Arial; margin-top:100px;">

        <h1>Good job, {name}!</h1>

        <h2>Question 2</h2>

        <p>Why are you interested in this field?</p>

        <textarea
            rows="6"
            cols="50"
            placeholder="Type your answer here..."
        ></textarea>

        <br><br>

        <button>Next Question</button>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
