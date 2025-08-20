from flask import Flask, render_template_string, request, redirect
import os

app = Flask(__name__)

# προσωρινή μνήμη για τις ερωτήσεις και απαντήσεις
questions = []

# φορτώνουμε το index.html σαν string
with open("index.html", "r", encoding="utf-8") as f:
    index_html_content = f.read()

@app.route("/")
def index():
    return render_template_string(index_html_content, questions=questions)

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    if question:
        questions.append({"question": question, "answers": []})
    return redirect("/")

@app.route("/answer/<int:qid>", methods=["POST"])
def answer(qid):
    answer = request.form.get("answer")
    if answer and 0 <= qid < len(questions):
        questions[qid]["answers"].append(answer)
    return redirect("/")

if __name__ == "__main__":
    # παίρνει το port από το Render ή default στο 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
