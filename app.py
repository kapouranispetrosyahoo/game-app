from flask import Flask, render_template, request, jsonify
import os
import openai
from dotenv import load_dotenv
from random import randint

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Αποθήκευση ερωτήσεων/απαντήσεων στη μνήμη
data = []

# Αυτόματο ψευδώνυμο
user_counter = 1

@app.route("/")
def index():
    global user_counter
    # Δημιουργία ψευδωνύμου
    username = f"Χρήστης {user_counter}"
    user_counter += 1
    return render_template("index.html", username=username)

@app.route("/submit_question", methods=["POST"])
def submit_question():
    content = request.json
    username = content.get("username")
    question = content.get("question")
    use_openai = content.get("use_openai", False)
    category = content.get("category", "")

    answer = ""
    if use_openai and question:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"[Κατηγορία: {category}] {question}",
                max_tokens=150
            )
            answer = response.choices[0].text.strip()
        except Exception as e:
            answer = f"Σφάλμα OpenAI: {str(e)}"

    # Αποθήκευση ερώτησης και απάντησης
    data.append({
        "username": username,
        "question": question,
        "answer": answer
    })

    return jsonify({"status": "success"})

@app.route("/get_data")
def get_data():
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
