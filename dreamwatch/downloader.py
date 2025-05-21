"""Functions for downloading YouTube audio using ``yt-dlp``."""

from pathlib import Path
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List, Optional


def download_audio(video_id: str, dst: Path) -> None:
    """Download a single video's audio to ``dst``.

    Parameters
    ----------
    video_id:
        The YouTube video identifier.
    dst:
        Destination directory for the downloaded file.
    """

    dst.mkdir(parents=True, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_tpl = str(dst / "%(_id)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f",
        "bestaudio",
        "--extract-audio",
        "--audio-format",
        "m4a",
        "-o",
        output_tpl,
        url,
    ]
    subprocess.run(cmd, check=True)


def fetch_video_ids(url: str, date_from: Optional[str], date_to: Optional[str]) -> List[str]:
    """Return video ids in ``url`` filtered by optional date range.

    Dates are strings in ``YYYYMMDD`` form. If ``None`` is provided the bound is
    ignored.
    """

    info_cmd = ["yt-dlp", "--flat-playlist", "-J", url]
    result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout or "{}")
    ids: List[str] = []
    for entry in data.get("entries", []):
        vid_id = entry.get("id")
        upload_date = entry.get("upload_date")
        if date_from and upload_date and upload_date < date_from:
            continue
        if date_to and upload_date and upload_date > date_to:
            continue
        if vid_id:
            ids.append(vid_id)
    return ids


def download_batch(
    url: str,
    date_from: Optional[str],
    date_to: Optional[str],
    dst: Path,
    threads: int = 2,
) -> None:
    """Download multiple videos' audio concurrently."""

    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    videos = fetch_video_ids(url, date_from, date_to)
    with ThreadPoolExecutor(max_workers=threads) as pool:
        for vid in videos:
            pool.submit(download_audio, vid, dst)
