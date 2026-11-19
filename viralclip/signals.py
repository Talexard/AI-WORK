"""Per-second "virality" signals. Every function returns a numpy array with one
value per second of video, already normalised to roughly 0..1 (0 = normal,
1 = extreme for this video)."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import numpy as np

SR = 16000


# ----------------------------------------------------------------- helpers
def rolling_median(x: np.ndarray, win: int) -> np.ndarray:
    """Rolling median over a centred window (fast enough for 1 value/sec)."""
    if len(x) == 0:
        return x
    pad = win // 2
    xp = np.pad(x, pad, mode="edge")
    view = np.lib.stride_tricks.sliding_window_view(xp, win)[: len(x)]
    return np.median(view, axis=1)


def robust_z(x: np.ndarray, baseline_win: int = 61) -> np.ndarray:
    """How unusual is each second compared with the surrounding minute?"""
    base = rolling_median(x, baseline_win)
    dev = x - base
    mad = np.median(np.abs(dev)) * 1.4826 + 1e-6
    return dev / mad


def squash(z: np.ndarray, lo: float = 1.0, hi: float = 5.0) -> np.ndarray:
    """Map z-scores to 0..1: below `lo` -> 0, above `hi` -> 1."""
    return np.clip((z - lo) / (hi - lo), 0, 1)


def smooth(x: np.ndarray, k: int = 3) -> np.ndarray:
    if k <= 1 or len(x) == 0:
        return x
    return np.convolve(x, np.ones(k) / k, mode="same")


# ----------------------------------------------------------------- audio
def load_audio(video: Path) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar",
         str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def audio_signals(video: Path, n: int, cache: Path | None = None) -> dict[str, np.ndarray]:
    """Loudness (yelling/explosions) and onset (sudden jump = scare/rage)."""
    if cache and cache.exists():
        db = np.load(cache)
    else:
        a = load_audio(video)
        hop = SR // 4  # 4 frames / second
        frames = len(a) // hop
        rms = np.sqrt(np.mean(a[: frames * hop].reshape(frames, hop) ** 2, axis=1) + 1e-10)
        db4 = 20 * np.log10(rms + 1e-6)
        # per second: use the loudest quarter-second (screams are short)
        secs = len(db4) // 4
        db = db4[: secs * 4].reshape(secs, 4).max(axis=1) if secs else np.zeros(0)
        if cache:
            np.save(cache, db)
    db = _fit(db, n, fill=float(np.median(db)) if len(db) else -60)
    loud = squash(robust_z(db, 61), 1.0, 4.5)
    # onset: next 1s vs previous 3s
    prev = np.array([db[max(0, i - 3): i].mean() if i > 0 else db[0] for i in range(n)])
    nxt = np.array([db[i: i + 2].max() for i in range(n)])
    onset = np.clip((nxt - prev - 6) / 12, 0, 1)  # +6dB starts counting, +18dB = max
    return {"loudness": loud, "onset": onset, "db": db}


# ----------------------------------------------------------------- chat
HYPE_CHAT = {
    # token(regex) : weight
    r"\blo+l+\b|\blmf?a+o+\b|\bkekw\b|\bomegalul\b|\blul\b|😂|🤣|\bhaha+\b|\bxd+\b": 1.0,
    r"💀|☠|\bdead\b|\bim dead\b": 1.2,
    r"\bclip (it|that)\b|\bclipped\b|\bclip\b": 1.5,
    r"\bno way\b|\bwtf\b|\bwhat+\b|\?{3,}|\bhow\b": 1.0,
    r"\bpog+(gers|champ)?\b|\bw+\b|\blets go+\b|\bgoat(ed)?\b|\binsane\b|\bcracked\b": 1.0,
    r"\bl+\b|\bf+\b|\bree+\b|\brip\b|\bomg\b|😱|😭|🔥": 0.8,
}
_HYPE_RX = [(re.compile(k, re.I), w) for k, w in HYPE_CHAT.items()]
LAUGH_RX = re.compile(r"\blo+l+\b|\blmf?a+o+\b|kekw|omegalul|😂|🤣|💀|haha", re.I)
CONFUSED_RX = re.compile(r"\?{2,}|\bwhat\b|\bwtf\b|\bhow\b", re.I)


def load_chat(path: Path) -> list[tuple[float, str]]:
    """Supports yt-dlp live_chat.json (JSON lines), TwitchDownloader JSON,
    or a simple CSV/TSV/JSON-list of (seconds, text)."""
    txt = path.read_text(encoding="utf-8", errors="ignore")
    msgs: list[tuple[float, str]] = []
    stripped = txt.lstrip()
    if stripped.startswith("{") and '"comments"' in txt[:5000]:  # TwitchDownloader
        for c in json.loads(txt).get("comments", []):
            msgs.append((float(c.get("content_offset_seconds", 0)),
                         (c.get("message") or {}).get("body", "")))
        return msgs
    if stripped.startswith("["):
        for m in json.loads(txt):
            msgs.append((float(m.get("t", m.get("time", 0))), m.get("text", "")))
        return msgs
    for line in txt.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("{"):  # yt-dlp live chat
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            r = o.get("replayChatItemAction", {})
            t = float(r.get("videoOffsetTimeMsec", 0)) / 1000
            for act in r.get("actions", []):
                item = act.get("addChatItemAction", {}).get("item", {})
                for key in ("liveChatTextMessageRenderer", "liveChatPaidMessageRenderer"):
                    rend = item.get(key)
                    if not rend:
                        continue
                    parts = []
                    for run in rend.get("message", {}).get("runs", []):
                        if "text" in run:
                            parts.append(run["text"])
                        elif "emoji" in run:
                            e = run["emoji"]
                            parts.append(e.get("emojiId", "") if len(e.get("emojiId", "")) <= 2
                                         else (e.get("shortcuts") or [""])[0])
                    msgs.append((t, " ".join(parts)))
        else:  # "12.5,message" / tab separated
            sep = "\t" if "\t" in line else ","
            a, _, b = line.partition(sep)
            try:
                msgs.append((float(a), b))
            except ValueError:
                continue
    return msgs


def chat_signals(msgs: list[tuple[float, str]], n: int, lag: float = 6.0) -> dict[str, np.ndarray]:
    """Chat velocity + hype words, shifted earlier by `lag` seconds because
    chat reacts after the moment happens."""
    vel = np.zeros(n)
    hype = np.zeros(n)
    laugh = np.zeros(n)
    confused = np.zeros(n)
    for t, text in msgs:
        i = int(t - lag)
        if 0 <= i < n:
            vel[i] += 1
            hype[i] += sum(w for rx, w in _HYPE_RX if rx.search(text))
            laugh[i] += bool(LAUGH_RX.search(text))
            confused[i] += bool(CONFUSED_RX.search(text))
    vel_s, hype_s = smooth(vel, 5), smooth(hype, 5)
    return {
        "chat_velocity": squash(robust_z(vel_s, 121), 1.5, 6),
        "chat_hype": squash(robust_z(hype_s, 121), 1.5, 6),
        "chat_laugh_frac": smooth(laugh, 5) / np.maximum(vel_s, 1e-6),
        "chat_confused_frac": smooth(confused, 5) / np.maximum(vel_s, 1e-6),
    }


# ----------------------------------------------------------------- heatmap
def heatmap_signal(heatmap: list[dict], n: int) -> np.ndarray:
    """YouTube 'Most Replayed' graph (values 0..1)."""
    out = np.zeros(n)
    for h in heatmap:
        a, b = int(h.get("start_time", 0)), int(h.get("end_time", 0))
        out[a:min(b + 1, n)] = h.get("value", 0)
    if out.max() <= 0:
        return out
    # only the replay peaks matter, not the general slope
    return squash(robust_z(out, 181), 0.5, 4)


# ----------------------------------------------------------------- speech
HYPE_SPEECH = {
    r"\boh my (god|gosh)\b|\bomg\b": 1.0,
    r"\bno+ way\b|\bno+o+\b": 1.0,
    r"\blet'?s go+\b|\blet'?s gooo*\b": 1.0,
    r"\bwhat+\b|\bwhat the\b|\bhuh\b": 0.7,
    r"\bbro+\b|\bdude\b|\bbruh\b": 0.5,
    r"\bf+u+c+k+\w*|\bsh+i+t+\w*|\bdamn\b|\bhell\b|\bholy\b": 1.0,
    r"\bclutch\b|\binsane\b|\bcrazy\b|\bunbelievable\b|\bimpossible\b": 1.0,
    r"\bi'?m (dead|dying|done)\b|\bhelp\b|\brun+\b|\bgo go\b": 0.8,
    r"\bwhy+\b|\bhow\b|\bare you (serious|kidding)\b": 0.6,
    r"\bha(ha)+\b|\blmao\b": 0.8,
}
_SPEECH_RX = [(re.compile(k, re.I), w) for k, w in HYPE_SPEECH.items()]
RAGE_RX = re.compile(r"f+u+c+k|sh+i+t|why+\b|are you (serious|kidding)|i'?m done|this game", re.I)
CLUTCH_RX = re.compile(r"let'?s go+|clutch|insane|no way|holy|oh my god|ace|one tap|w\b", re.I)
SCARE_RX = re.compile(r"\bwhat was that\b|\brun\b|\bnope\b|\bhelp\b|\bscared\b|\bjump", re.I)


def speech_signals(words: list[dict], n: int) -> dict[str, np.ndarray]:
    hype = np.zeros(n)
    rate = np.zeros(n)
    caps = np.zeros(n)
    for w in words:
        i = int(w["start"])
        if not 0 <= i < n:
            continue
        rate[i] += 1
        txt = w["word"]
        hype[i] += sum(wt for rx, wt in _SPEECH_RX if rx.search(txt))
        caps[i] += txt.endswith("!")
    # two-word phrases ("no way", "oh my god", "let's go")
    for a, b, c in zip(words, words[1:], words[2:] + [{"word": ""}]):
        phrase = f"{a['word']} {b['word']} {c['word']}"
        i = int(a["start"])
        if 0 <= i < n:
            for rx, wt in _SPEECH_RX:
                if " " in rx.pattern and rx.search(phrase):
                    hype[i] += wt * 0.5
    hype_s = smooth(hype + caps * 0.5, 3)
    talk = smooth(rate, 3)
    return {
        "speech_hype": np.clip(hype_s / 1.5, 0, 1),
        "speech_rate": squash(robust_z(talk, 61), 1.0, 4.0),
    }


# ----------------------------------------------------------------- scenes
def scene_signal(video: Path, n: int, cache: Path | None = None) -> np.ndarray:
    """Density of hard cuts / big visual changes (explosions, deaths, flashes)."""
    if cache and cache.exists():
        times = np.load(cache)
    else:
        res = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(video), "-an", "-vf",
             "fps=4,scale=160:-2,select='gt(scene,0.35)',showinfo", "-f", "null", "-"],
            capture_output=True, text=True)
        times = np.array([float(m) for m in re.findall(r"pts_time:([\d.]+)", res.stderr)])
        if cache:
            np.save(cache, times)
    out = np.zeros(n)
    for t in times:
        if int(t) < n:
            out[int(t)] += 1
    return np.clip(smooth(out, 5) * 2, 0, 1)


def _fit(x: np.ndarray, n: int, fill: float = 0.0) -> np.ndarray:
    if len(x) >= n:
        return x[:n]
    return np.concatenate([x, np.full(n - len(x), fill)])
