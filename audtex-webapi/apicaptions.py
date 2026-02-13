from flask import Flask, request, jsonify, send_file
import os
from captions import generate_captions

app = Flask(__name__)

UPLOAD_FOLDER = "temp"
OUTPUT_FOLDER = "result"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "AudTex AI API Running"

@app.route("/generate", methods=["POST"])
def generate():
    if "video" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    video = request.files["video"]
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    output_video = generate_captions(video_path)

    return send_file(output_video, as_attachment=True)

if __name__ == "__main__":
    app.run()
