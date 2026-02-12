"use client";
import { useState } from "react";

export default function Home() {

  const [loading, setLoading] = useState(false);
  const [video, setVideo] = useState(null);

  async function uploadVideo() {

    if (!video) {
      alert("Please choose a video first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("video", video);

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData
    });

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = "captioned.mp4";
    a.click();

    setLoading(false);
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 bg-black text-white">

      <h1 className="text-4xl font-bold mb-6 text-yellow-400">
        AI Shorts Caption Generator
      </h1>

      <div className="bg-zinc-900 p-8 rounded-2xl shadow-lg w-full max-w-md">

        <input
          type="file"
          accept="video/*"
          onChange={(e) => setVideo(e.target.files[0])}
          className="mb-6 w-full"
        />

        <button
          onClick={uploadVideo}
          className="w-full bg-yellow-400 text-black py-3 rounded-xl font-bold hover:bg-yellow-500"
        >
          {loading ? "Processing..." : "Generate Captions"}
        </button>

      </div>

    </main>
  );
}
