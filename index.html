from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Ορίστε το API key ως μεταβλητή περιβάλλοντος
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")

    # Κλήση στο OpenAI API
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return jsonify({
        "response": response.choices[0].message["content"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
