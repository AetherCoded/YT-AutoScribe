from pathlib import Path


def whisper_transcribe(path: Path):
    """Placeholder for whisper transcription."""
    # TODO: integrate with Ollama
    return []


def diarize(segments):
    """Placeholder for speaker diarization."""
    # TODO: call pyannote
    return []


def transcribe_file(path: Path):
    segments = whisper_transcribe(path)
    diar = diarize(segments)
    # TODO: save as JSON
    return diar


def transcribe_batch(folder: Path):
    folder = Path(folder)
    for audio in folder.glob('*.m4a'):
        transcribe_file(audio)
