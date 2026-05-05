from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # ✅ Allow frontend requests

# Config Class
class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = "https://openrouter.ai/api/v1"
    MODEL = "openai/gpt-4o-mini"

    @staticmethod
    def validate():
        if not Config.OPENROUTER_API_KEY:
            raise ValueError("❌ OPENROUTER_API_KEY not found in .env")

Config.validate()

# OpenAI Client
client = OpenAI(
    api_key=Config.OPENROUTER_API_KEY,
    base_url=Config.BASE_URL
)

# AI Function
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


# Routes
@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "🚀 AI Log Analyzer API is live"
    })


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