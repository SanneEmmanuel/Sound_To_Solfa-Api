import numpy as np
import librosa

# Solfa syllables for C major scale
SOLFA_SYLLABLES = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti']

def midi_to_solfa(midi_note: int) -> str:
    """
    Convert a MIDI note number to the closest solfa syllable assuming C major scale.
    """
    pitch_class = midi_note % 12
    scale_pitch_classes = [0, 2, 4, 5, 7, 9, 11]  # C D E F G A B
    closest_index = min(range(len(scale_pitch_classes)), key=lambda i: abs(scale_pitch_classes[i] - pitch_class))
    return SOLFA_SYLLABLES[closest_index]

def extract_pitch(y_segment: np.ndarray, sr: int) -> float | None:
    """
    Extract median pitch in Hz from an audio segment using librosa's piptrack.
    Returns None if no pitch detected.
    """
    pitches, magnitudes = librosa.piptrack(y=y_segment, sr=sr)
    pitch_values = []

    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)

    if not pitch_values:
        return None

    return float(np.median(pitch_values))
