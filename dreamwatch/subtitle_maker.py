from pathlib import Path


def build_srt(transcript, speaker_map):
    """Placeholder for building SRT subtitles from transcript."""
    # TODO: implement SRT generation
    return ""


def subtitle_batch(folder: Path, speaker_map):
    folder = Path(folder)
    for json_file in folder.glob('*.json'):
        # TODO: parse JSON and build SRT
        build_srt({}, speaker_map)
