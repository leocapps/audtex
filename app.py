from flask import Flask, render_template, request, send_file
import os
from faster_whisper import WhisperModel
import subprocess
from captions import make_shorts_captions

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("Loading AI model (first time takes 2-5 minutes)...")
model = WhisperModel("base", compute_type="int8")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    video = request.files["video"]

    input_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(input_path)

    audio_path = os.path.join(UPLOAD_FOLDER, "audio.wav")

    # extract audio
    subprocess.run([
        "ffmpeg","-y","-i",input_path,
        "-ar","16000","-ac","1",audio_path
    ])

    # transcribe
    segments, info = model.transcribe(audio_path)

    segs = []
    for s in segments:
        segs.append({
            "start": s.start,
            "end": s.end,
            "text": s.text
        })

    output_video = os.path.join(OUTPUT_FOLDER, "captioned.mp4")

    make_shorts_captions(input_path, segs, output_video)

    return send_file(output_video, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

