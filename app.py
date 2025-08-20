from flask import Flask, request, render_template_string
import openai
import os

app = Flask(__name__)

# Βάλε το δικό σου API key εδώ ή ως περιβαλλοντική μεταβλητή
openai.api_key = os.getenv("OPENAI_API_KEY")

html_template = """
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask OpenAI Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 100px; }
        button { padding: 10px 20px; margin-top: 10px; cursor: pointer; }
        .response { margin-top: 20px; background: #eaeaea; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Ρώτα κάτι στο OpenAI</h2>
        <form method="POST">
            <textarea name="user_input" placeholder="Γράψε εδώ την ερώτησή σου"></textarea>
            <br>
            <button type="submit">Στείλε</button>
        </form>
        {% if response %}
            <div class="response">
                <strong>Απάντηση:</strong>
                <p>{{ response }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            # Κλήση στο OpenAI
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}],
            )
            response = completion.choices[0].message.content
    return render_template_string(html_template, response=response)

if __name__ == "__main__":
    app.run(debug=True)
