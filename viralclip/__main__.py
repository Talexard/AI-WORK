"""viralclip: scan a YouTube video / stream VOD and cut 20-30 viral vertical clips.

    python -m viralclip "https://www.youtube.com/watch?v=..." --count 25
    python -m viralclip vod.mp4 --chat chat.json --layout facecam --facecam 0.72,0.70,0.27,0.29
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import numpy as np

from . import signals as S
from .detect import DEFAULT_WEIGHTS, detect
from .fetch import fetch
from .render import render, slug
from .transcribe import all_words, find_youtube_captions, from_youtube_json3, transcribe


def hms(t: float) -> str:
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="viralclip", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="YouTube URL or local video file")
    ap.add_argument("-o", "--out", default="clips_out", help="output folder")
    ap.add_argument("-n", "--count", type=int, default=25, help="clips to make (default 25)")
    ap.add_argument("--min-len", type=float, default=15)
    ap.add_argument("--max-len", type=float, default=60)
    ap.add_argument("--chat", help="chat log for local files (yt-dlp live_chat.json, "
                                   "TwitchDownloader JSON, or 'seconds,text' CSV)")
    ap.add_argument("--chat-lag", type=float, default=6.0, help="seconds chat lags the moment")
    ap.add_argument("--cookies"), ap.add_argument("--cookies-from-browser")
    ap.add_argument("--whisper-model", default="small", help="tiny/base/small/medium/large-v3")
    ap.add_argument("--language", default=None)
    ap.add_argument("--no-transcribe", action="store_true")
    ap.add_argument("--whisper", action="store_true",
                    help="always use Whisper even if YouTube captions exist (slower, more accurate)")
    ap.add_argument("--transcript", help="use an existing transcript JSON (same format)")
    ap.add_argument("--scenes", action="store_true", help="also use scene-cut density (slower)")
    ap.add_argument("--ai", action="store_true", help="re-rank & write hooks with Claude")
    ap.add_argument("--game", default="", help="game name hint for hooks/hashtags")
    ap.add_argument("--layout", choices=["blur", "crop", "facecam"], default="blur")
    ap.add_argument("--zoom", type=float, default=1.25, help="gameplay zoom in blur layout")
    ap.add_argument("--facecam", help="x,y,w,h of the facecam as fractions of the frame")
    ap.add_argument("--font", default="Inter Display")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="find clips but don't render")
    ap.add_argument("--weights", help='JSON to override signal weights, e.g. \'{"loudness":0.3}\'')
    a = ap.parse_args(argv)

    out = Path(a.out)
    work = out / "_work"
    t0 = time.time()

    print("[1/5] Fetching source…")
    src = fetch(a.source, work, a.cookies, a.cookies_from_browser, chat_file=a.chat)
    n = int(src.duration) + 1
    print(f"      {src.title!r}  ({hms(src.duration)})")

    print("[2/5] Transcribing…")
    transcript = {"segments": []}
    if a.transcript:
        transcript = json.loads(Path(a.transcript).read_text())
    elif not a.no_transcribe and not a.whisper and find_youtube_captions(work):
        cap = find_youtube_captions(work)
        print(f"      using YouTube captions ({cap.name})")
        transcript = from_youtube_json3(cap)
    elif not a.no_transcribe:
        transcript = transcribe(src.video, work / "transcript.json", a.whisper_model, a.language)
    words = all_words(transcript)
    print(f"      {len(words)} words")

    print("[3/5] Measuring signals…")
    sig = S.audio_signals(src.video, n, work / "audio_db.npy")
    used = ["audio"]
    if src.chat_file and Path(src.chat_file).exists():
        msgs = S.load_chat(Path(src.chat_file))
        sig.update(S.chat_signals(msgs, n, a.chat_lag))
        used.append(f"chat ({len(msgs)} msgs)")
    if src.heatmap:
        sig["heatmap"] = S.heatmap_signal(src.heatmap, n)
        used.append("most-replayed heatmap")
    if words:
        sig.update(S.speech_signals(words, n))
        used.append("speech")
    if a.scenes:
        sig["scenes"] = S.scene_signal(src.video, n, work / "scenes.npy")
        used.append("scenes")
    print("      using: " + ", ".join(used))

    print("[4/5] Finding moments…")
    weights = dict(DEFAULT_WEIGHTS)
    if a.weights:
        weights.update(json.loads(a.weights))
    clips, score = detect(sig, transcript, words, src.duration, a.count, a.min_len,
                          a.max_len, weights, pool_factor=2.0 if a.ai else 1.3)
    if a.ai and clips:
        from .llm import rerank
        pool = clips[: max(a.count + 15, int(a.count * 1.8))]
        print(f"      asking Claude to judge {len(pool)} candidates…")
        clips = rerank(pool, src.title, src.uploader, a.game)
    clips = clips[: a.count]
    clips.sort(key=lambda c: c.score, reverse=True)
    if len(clips) < a.count:
        print(f"      note: only {len(clips)} distinct moments found "
              f"(video too short or too calm for {a.count}).")
    weak = sum(c.score < 0.12 for c in clips)
    if weak:
        print(f"      note: {weak} clips have weak signals; post the top ones first.")

    facecam = tuple(float(x) for x in a.facecam.split(",")) if a.facecam else None
    print(f"[5/5] Rendering {len(clips)} clips → {out}/")
    rows = []
    for rank, c in enumerate(clips, 1):
        name = f"{rank:02d}_{c.archetype}_{slug(c.hook or c.quote)}.mp4"
        if not a.dry_run:
            render(src.video, c, words, out / name, a.layout, a.zoom, facecam, a.font,
                   not a.no_captions)
        d = c.to_dict()
        d.update(rank=rank, file=name, start_hms=hms(c.start), end_hms=hms(c.end))
        if src.url and "youtu" in src.url:
            sep = "&" if "?" in src.url else "?"
            d["link"] = f"{src.url}{sep}t={int(c.start)}s"
        rows.append(d)
        print(f"   #{rank:02d} {hms(c.start)}-{hms(c.end)} ({c.duration:4.1f}s) "
              f"score={c.score:.3f} {c.archetype:6s} {c.hook}")

    (out / "clips.json").write_text(json.dumps(
        {"title": src.title, "source": a.source, "duration": src.duration,
         "signals_used": used, "clips": rows}, indent=2, ensure_ascii=False))
    with open(out / "clips.csv", "w", newline="", encoding="utf-8") as f:
        cols = ["rank", "file", "start_hms", "end_hms", "duration", "score", "archetype",
                "hook", "quote", "reasons"]
        wr = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        for r in rows:
            wr.writerow({**r, "reasons": "; ".join(r["reasons"])})
    np.save(work / "score.npy", score)
    print(f"Done in {time.time() - t0:.0f}s. See {out / 'clips.csv'}")


if __name__ == "__main__":
    main()
