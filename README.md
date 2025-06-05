````markdown
# SoundToSolfa-api 🎵🎶

**SoundToSolfa-api** is a FastAPI-based web service that analyzes short audio clips (like melodies played with a metronome) and converts them into **solfa notation** — the familiar Do, Re, Mi system used for singing and music education.

---

## 🎯 Purpose

This API is designed to help musicians, educators, and developers:

- Transcribe monophonic melodies into solfa syllables automatically  
- Understand the rhythm by detecting note durations in beats  
- Use solfa notation for music learning, transcription, or further processing  

Whether you want to build music education tools, melody analyzers, or just experiment with pitch recognition, **SoundToSolfa-api** gives you a simple, automated solution.

---

## 🚀 Features

- Accepts up to 15 seconds of audio input with metronome ticks  
- Detects note onsets and estimates tempo  
- Extracts pitch and maps it to solfa syllables in C major scale  
- Returns each note with its relative duration in beats (e.g., half-beat, one beat)  
- Lightweight, fast, and easy to deploy  

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.9+  
- `pip` package manager

### Installation

Clone the repository:

```bash
git clone https://github.com/SanneEmmanuel/Sound_To_Solfa-Api.git
cd Sound_To_Solfa-Api
````

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Locally

Start the FastAPI server with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Your API will be accessible at:

```
http://localhost:8000/api/solfa/analyze
```

### API Usage

Send a POST request with an audio file (`.wav`, `.mp3`, etc.) under the form field `audio`:

Example using `curl`:

```bash
curl -X POST "http://localhost:8000/api/solfa/analyze" -F "audio=@your_audio_file.wav"
```

Response JSON example:

```json
{
  "notes": [
    {"solfa": "Do", "beats": 1.0},
    {"solfa": "Re", "beats": 0.5},
    {"solfa": "Mi", "beats": 1.0},
    {"solfa": "Fa", "beats": 0.25}
  ]
}
```

---

## ☁️ Deployment

You can deploy this API easily on [Render.com](https://render.com) or other cloud platforms.

Use the provided `render.yaml` config for easy setup with Render.

---

## 🛠️ Project Structure

```
Sound_To_Solfa-Api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entrypoint
│   └── utils.py         # Helper functions
├── requirements.txt     # Python dependencies
├── render.yaml          # Deployment config for Render.com
├── runtime.txt          # Python runtime version
└── README.md            # This file
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a GitHub issue or submit a pull request.

---

## 📜 License

MIT License © 2025 Dr. Sanne Karibo

---

## 🙏 Acknowledgments

* Built with [FastAPI](https://fastapi.tiangolo.com/) and [Librosa](https://librosa.org/)
* Inspired by music education and solfa notation systems

---

## 🔗 Links

* GitHub Repository: [https://github.com/SanneEmmanuel/Sound\_To\_Solfa-Api](https://github.com/SanneEmmanuel/Sound_To_Solfa-Api/tree/main)

---

Feel free to reach out if you want help deploying or customizing this API!

---

**Happy Solfa-ing! 🎼🎤**
— Dr. Sanne Karibo

```
```
