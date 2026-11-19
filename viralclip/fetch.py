"""Download a YouTube video plus everything useful for finding highlights:
the video file, its metadata (including the "Most Replayed" heatmap), and the
live-chat replay when the video was a livestream."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Source:
    video: Path
    workdir: Path
    title: str = ""
    url: str = ""
    duration: float = 0.0
    heatmap: list[dict] = field(default_factory=list)
    chat_file: Path | None = None
    uploader: str = ""


def probe_duration(video: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(video)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out or 0)


def fetch(url_or_path: str, workdir: Path, cookies: str | None = None,
          cookies_from_browser: str | None = None, max_height: int = 1080,
          chat_file: str | None = None) -> Source:
    workdir.mkdir(parents=True, exist_ok=True)
    p = Path(url_or_path)
    if p.exists():  # local file
        src = Source(video=p.resolve(), workdir=workdir, title=p.stem,
                     duration=probe_duration(p))
        if chat_file:
            src.chat_file = Path(chat_file)
        return src

    base = ["yt-dlp", "--no-playlist", "-o", str(workdir / "source.%(ext)s")]
    if cookies:
        base += ["--cookies", cookies]
    if cookies_from_browser:
        base += ["--cookies-from-browser", cookies_from_browser]

    # 1) metadata (heatmap lives here)
    info_raw = subprocess.run(base + ["-J", url_or_path], capture_output=True,
                              text=True)
    if info_raw.returncode != 0:
        raise SystemExit(
            "yt-dlp could not read the video.\n" + info_raw.stderr[-1500:] +
            "\nTip: YouTube often blocks servers/cloud IPs. Run this on your own "
            "computer, or pass --cookies-from-browser chrome / --cookies cookies.txt")
    info = json.loads(info_raw.stdout)
    (workdir / "info.json").write_text(json.dumps(info))

    # 2) the video itself
    fmt = (f"bv*[height<={max_height}][ext=mp4]+ba[ext=m4a]/"
           f"b[height<={max_height}]/bv*+ba/b")
    subprocess.run(base + ["-f", fmt, "--merge-output-format", "mp4",
                           url_or_path], check=True)
    video = next(workdir.glob("source.mp4"), None) or next(workdir.glob("source.*"))

    # 3) live chat replay (only exists for past livestreams)
    chat = None
    if info.get("was_live") or info.get("live_status") == "was_live" or \
            "live_chat" in (info.get("subtitles") or {}):
        subprocess.run(base + ["--skip-download", "--write-subs",
                               "--sub-langs", "live_chat", url_or_path])
        chat = next(workdir.glob("source*.live_chat.json"), None)

    # 4) YouTube's own captions (word-timed) - instant alternative to Whisper
    subprocess.run(base + ["--skip-download", "--write-auto-subs", "--write-subs",
                           "--sub-langs", "en.*,en", "--sub-format", "json3",
                           url_or_path])

    return Source(
        video=video, workdir=workdir, title=info.get("title", ""), url=url_or_path,
        duration=float(info.get("duration") or probe_duration(video)),
        heatmap=info.get("heatmap") or [], chat_file=Path(chat_file) if chat_file else chat,
        uploader=info.get("uploader") or info.get("channel") or "")
