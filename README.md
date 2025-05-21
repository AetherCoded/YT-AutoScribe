# YT-AutoScribe

This project aims to build a Windows desktop tool that downloads audio from YouTube,
transcribes it locally using Whisper via Ollama with speaker diarisation,
and converts the transcripts into colour-coded SRT subtitle files.

The repository currently contains a minimal GUI with a working downloader pane.
Downloads are performed using `yt-dlp` and saved into the `downloads/` folder by
default. Ensure that the `yt-dlp` executable is installed and available on your
`PATH` so the application can invoke it.

## Installation

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

Then run the GUI with:

```bash
python dreamwatch.py
```
