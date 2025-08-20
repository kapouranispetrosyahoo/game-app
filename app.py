from flask import Flask
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/test_openai")
def test_openai():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        return f"OpenAI API δουλεύει! Response: {response.choices[0].message.content}"
    except Exception as e:
        return f"Κάτι πήγε στραβά: {e}"

if __name__ == "__main__":
    app.run(debug=True)
