from flask import Flask, render_template_string, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "ένα_τυχαίο_μυστικό_κλειδί"

# προσωρινή μνήμη για τις ερωτήσεις και απαντήσεις
questions = []

# φορτώνουμε το index.html σαν string
with open("index.html", "r", encoding="utf-8") as f:
    index_html_content = f.read()

# κάθε χρήστης παίρνει nickname αν δεν έχει
@app.before_request
def set_nickname():
    if "nickname" not in session:
        session["nickname"] = f"User{random.randint(1000,9999)}"

@app.route("/")
def index():
    return render_template_string(index_html_content, questions=questions, nickname=session["nickname"])

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    if question:
        # αποθηκεύουμε και το nickname του χρήστη
        questions.append({"question": question, "answers": [], "nickname": session["nickname"]})
    return redirect("/")

@app.route("/answer/<int:qid>", methods=["POST"])
def answer(qid):
    answer = request.form.get("answer")
    if answer and 0 <= qid < len(questions):
        # αποθηκεύουμε και ποιος απάντησε
        questions[qid]["answers"].append({"answer": answer, "nickname": session["nickname"]})
    return redirect("/")

# route για αλλαγή nickname
@app.route("/set_nickname", methods=["POST"])
def set_nickname_post():
    data = request.get_json()
    nickname = data.get("nickname")
    if nickname:
        session["nickname"] = nickname
    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
