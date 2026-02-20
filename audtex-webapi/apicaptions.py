from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from captions import generate_captions

app = Flask(__name__)

# 🔥 Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def home():
    return "AudTex Caption API Running Successfully!"


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        result = generate_captions(text)

        return jsonify({
            "status": "success",
            "captions": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)