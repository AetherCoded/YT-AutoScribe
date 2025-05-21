"""Functions for downloading YouTube audio using ``yt-dlp``."""

from pathlib import Path
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List, Optional, Tuple


class YtDlpNotFoundError(RuntimeError):
    """Raised when the ``yt-dlp`` executable is missing."""


def _run(cmd: Iterable[str], **kwargs) -> subprocess.CompletedProcess:
    """Wrapper around :func:`subprocess.run` that provides a clearer error.

    Parameters
    ----------
    cmd:
        Command list to execute.
    kwargs:
        Additional arguments passed to :func:`subprocess.run`.
    """

    try:
        return subprocess.run(cmd, **kwargs)
    except FileNotFoundError as exc:
        raise YtDlpNotFoundError(
            "yt-dlp executable not found. Install yt-dlp and ensure it is on your PATH."
        ) from exc


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
    # use the video ID for a unique filename
    output_tpl = str(dst / "%(id)s.%(ext)s")
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
    _run(cmd, check=True)


def fetch_video_ids(url: str, date_from: Optional[str], date_to: Optional[str]) -> List[str]:
    """Return video ids in ``url`` filtered by optional date range.

    Dates are strings in ``YYYYMMDD`` form. If ``None`` is provided the bound is
    ignored.
    """

    info_cmd = ["yt-dlp", "--flat-playlist", "-J", url]
    try:
        result = _run(info_cmd, capture_output=True, text=True, check=True)
    except YtDlpNotFoundError as exc:
        raise exc
    except subprocess.CalledProcessError:
        return []
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
    try:
        videos = fetch_video_ids(url, date_from, date_to)
    except YtDlpNotFoundError as exc:
        raise exc
    with ThreadPoolExecutor(max_workers=threads) as pool:
        for vid in videos:
            pool.submit(download_audio, vid, dst)


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """Return whether ``url`` is a valid YouTube playlist/URL.

    If valid, also return a suggested folder name derived from the channel and
    playlist title. The folder name is stripped of spaces and truncated to keep
    it short.
    """

    info_cmd = ["yt-dlp", "-J", url]
    try:
        result = _run(info_cmd, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, YtDlpNotFoundError):
        return False, None

    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return False, None

    entries = data.get("entries")
    if not entries:
        return False, None

    uploader = data.get("uploader", "")
    title = data.get("title", "")
    # Compose a folder name such as ``Uploader_Title`` and remove spaces.
    folder_name = f"{uploader}_{title}".replace(" ", "") or "NewProject"
    # Truncate to a reasonable length
    folder_name = folder_name[:30]
    return True, folder_name
