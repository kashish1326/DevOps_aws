from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = "llama-3.3-70b-versatile" # Free model on Groq

    @staticmethod
    def validate():
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found")

Config.validate()

client = Groq(api_key=Config.GROQ_API_KEY)

def analyze_with_ai(logs: str) -> str:
    try:
        response = client.chat.completions.create(
            model=Config.MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert DevOps engineer.\n"
                        "Analyze logs and respond in this format:\n\n"
                        "🔍 Summary:\n"
                        "⚠️ Errors:\n"
                        "💡 Suggestions:\n"
                    )
                },
                {"role": "user", "content": logs}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route("/analyze", methods=["POST"])
def analyze_logs():
    try:
        data = request.get_json()

        if not data or "logs" not in data:
            return jsonify({"error": "Logs are required"}), 400

        logs = data["logs"]

        if len(logs.strip()) == 0:
            return jsonify({"error": "Logs cannot be empty"}), 400

        analysis = analyze_with_ai(logs)

        return jsonify({
            "success": True,
            "analysis": analysis
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)