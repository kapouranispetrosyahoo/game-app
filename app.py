from flask import Flask, render_template_string, request, redirect, session
import openai
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Αλλάξε το σε κάτι ασφαλές για παραγωγή

# Ρύθμισε εδώ το OpenAI API key σου
openai.api_key = os.getenv("OPENAI_API_KEY")

questions = []

# Φόρτωση του index.html
with open("index.html", "r", encoding="utf-8") as f:
    index_html_content = f.read()

def generate_ai_nickname():
    """Ζητάει από το OpenAI API ένα διασκεδαστικό AI-themed nickname."""
    prompt = "Give me a fun, short, AI-themed nickname, one word only."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=5,
        temperature=0.8
    )
    nickname = response.choices[0].text.strip()
    return nickname or "AI_User"

@app.before_request
def ensure_nickname():
    """Βάζει nickname στη συνεδρία αν δεν υπάρχει."""
    if "nickname" not in session:
        session["nickname"] = generate_ai_nickname()

@app.route("/")
def index():
    return render_template_string(index_html_content, questions=questions, nickname=session["nickname"])

@app.route("/set_nickname", methods=["POST"])
def set_nickname():
    nickname = request.form.get("nickname")
    if nickname:
        session["nickname"] = nickname
    return redirect("/")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    if question:
        questions.append({"question": question, "nickname": session["nickname"], "answers": []})
    return redirect("/")

@app.route("/answer/<int:qid>", methods=["POST"])
def answer(qid):
    answer = request.form.get("answer")
    if answer and 0 <= qid < len(questions):
        questions[qid]["answers"].append({"answer": answer, "nickname": session["nickname"]})
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
