from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def download_audio(video_id: str, dst: Path):
    """Placeholder for downloading a single video's audio."""
    # TODO: implement with yt-dlp
    pass


def fetch_video_ids(url: str, date_from: str, date_to: str):
    """Placeholder for fetching video ids within a date range."""
    # TODO: implement playlist parsing
    return []


def download_batch(url: str, date_from: str, date_to: str, dst: Path, threads: int = 2):
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    videos = fetch_video_ids(url, date_from, date_to)
    with ThreadPoolExecutor(max_workers=threads) as pool:
        for vid in videos:
            pool.submit(download_audio, vid, dst)
