from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key="YOUR_API_KEY")  # Βάλε εδώ το δικό σου API key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_nickname", methods=["POST"])
def get_nickname():
    user_input = request.form.get("user_input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Κλήση στο OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )

    nickname = response.choices[0].message.content
    return jsonify({"nickname": nickname})

if __name__ == "__main__":
    app.run(debug=True)