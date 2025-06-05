from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # <-- add this import
import numpy as np
import librosa
import io

app = FastAPI()

# Add CORS middleware allowing all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # allow all headers
)

# Map MIDI notes in C major scale to solfa
SOLFA_SYLLABLES = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti']

def midi_to_solfa(midi_note):
    pitch_class = midi_note % 12
    # C major scale pitch classes: C=0, D=2, E=4, F=5, G=7, A=9, B=11
    scale_pitch_classes = [0, 2, 4, 5, 7, 9, 11]
    closest_index = min(range(len(scale_pitch_classes)), key=lambda i: abs(scale_pitch_classes[i] - pitch_class))
    return SOLFA_SYLLABLES[closest_index]

@app.post("/api/solfa/analyze")
async def analyze_audio(audio: UploadFile = File(...)):
    if not audio.content_type.startswith('audio'):
        raise HTTPException(status_code=400, detail="Invalid file type, please upload audio.")

    data = await audio.read()
    audio_buffer = io.BytesIO(data)

    y, sr = librosa.load(audio_buffer, sr=None, mono=True)

    # Estimate tempo (BPM) and beat frames
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    if tempo == 0:
        # fallback if tempo can't be estimated, use 60 BPM
        tempo = 60

    beat_duration_sec = 60.0 / tempo

    # Onset detection (note start times)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    notes = []

    for i in range(len(onset_times)):
        start = onset_times[i]
        end = onset_times[i+1] if i+1 < len(onset_times) else len(y)/sr
        segment = y[int(start*sr):int(end*sr)]

        if len(segment) == 0:
            continue

        pitches, magnitudes = librosa.piptrack(y=segment, sr=sr)
        pitch_values = []

        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)

        if not pitch_values:
            continue

        median_pitch_hz = np.median(pitch_values)
        midi_note = librosa.hz_to_midi(median_pitch_hz)
        solfa = midi_to_solfa(int(round(midi_note)))

        # Calculate duration in beats (relative to tempo)
        duration_sec = end - start
        duration_beats = duration_sec / beat_duration_sec

        # Round duration beats to nearest common fraction (optional)
        duration_beats_rounded = round(duration_beats * 4) / 4  # quarter beat precision

        notes.append({
            "solfa": solfa,
            "beats": duration_beats_rounded
        })

    return JSONResponse(content={"notes": notes})
