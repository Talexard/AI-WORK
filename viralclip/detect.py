"""Turn per-second signals into ranked clip candidates."""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict

import numpy as np

from .signals import RAGE_RX, CLUTCH_RX, SCARE_RX, smooth

# Default weights. Missing signals are dropped and the rest re-normalised,
# so a video without chat still scores on audio + speech + heatmap.
DEFAULT_WEIGHTS = {
    "chat_velocity": 0.22,
    "chat_hype": 0.18,
    "heatmap": 0.20,
    "loudness": 0.16,
    "onset": 0.08,
    "speech_hype": 0.10,
    "speech_rate": 0.03,
    "scenes": 0.03,
}

# How much setup (seconds before the peak) and reaction (after) each type needs
ARCHETYPE_TIMING = {
    "rage":   (8, 6),
    "clutch": (16, 5),
    "funny":  (10, 5),
    "scare":  (9, 5),
    "wtf":    (10, 5),
    "story":  (22, 5),
    "hype":   (12, 5),
}

HOOK_TEMPLATES = {
    "rage":   ["He completely lost it 💀", "This game broke him 😭", "Rage level: 100"],
    "clutch": ["This should NOT have worked 🤯", "The most insane clutch 😳", "Watch till the end"],
    "funny":  ["I can't stop laughing 😂", "He did NOT just do that 💀", "Worst timing ever 😭"],
    "scare":  ["He was NOT ready 😱", "Turn your volume up 😳", "That scream though 💀"],
    "wtf":    ["Wait… what just happened?? 🤨", "Nobody can explain this", "How is this possible"],
    "story":  ["You have to hear this 👀", "He really said this 😳", "Chat went crazy"],
    "hype":   ["Chat went INSANE 🔥", "This moment was crazy", "Wait for it…"],
}


@dataclass
class Clip:
    start: float
    end: float
    peak: float
    score: float
    archetype: str = "hype"
    hook: str = ""
    quote: str = ""
    transcript: str = ""
    reasons: list[str] = field(default_factory=list)
    signals: dict = field(default_factory=dict)
    llm: dict | None = None

    @property
    def duration(self) -> float:
        return self.end - self.start

    def to_dict(self) -> dict:
        d = asdict(self)
        d["duration"] = round(self.duration, 2)
        return d


def combine(sig: dict[str, np.ndarray], weights: dict[str, float]) -> np.ndarray:
    present = {k: w for k, w in weights.items() if k in sig and np.any(sig[k] > 0)}
    total = sum(present.values()) or 1.0
    n = len(next(iter(sig.values())))
    score = np.zeros(n)
    for k, w in present.items():
        score += sig[k] * (w / total)
    # Agreement bonus: moments where several independent signals fire together
    # are far more likely to be real highlights than one noisy spike.
    active = sum((sig[k] > 0.35).astype(float) for k in present)
    score *= 1 + 0.15 * np.clip(active - 1, 0, 4)
    return smooth(score, 3)


def find_peaks(score: np.ndarray, min_gap: int, k: int) -> list[int]:
    order = np.argsort(score)[::-1]
    taken: list[int] = []
    for i in order:
        if score[i] <= 0:
            break
        if all(abs(i - j) >= min_gap for j in taken):
            taken.append(int(i))
        if len(taken) >= k:
            break
    return taken


def _segments(transcript: dict) -> list[dict]:
    return transcript.get("segments", []) if transcript else []


def snap_start(t: float, segs: list[dict], max_shift: float = 4.0) -> float:
    """Move start to the beginning of the sentence it lands in (or just after
    the previous one ends) so clips don't open mid-word."""
    best = t
    for s in segs:
        if s["start"] <= t <= s["end"] and t - s["start"] <= max_shift:
            return s["start"]
        if 0 <= s["start"] - t <= 1.5:
            best = s["start"]
            break
    return best


def snap_end(t: float, segs: list[dict], max_shift: float = 4.0) -> float:
    for s in segs:
        if s["start"] <= t <= s["end"] and s["end"] - t <= max_shift:
            return s["end"] + 0.3
    return t


def reaction_end(db: np.ndarray, peak: int, default_post: int, max_post: int = 15) -> int:
    """Extend past the peak while it's still loud (the reaction), stop when
    loudness falls back toward the local baseline."""
    if db is None or len(db) == 0:
        return peak + default_post
    lo = max(0, peak - 60)
    base = np.median(db[lo:peak + 1]) if peak > lo else db[peak]
    end = peak + default_post
    for i in range(peak + 1, min(len(db), peak + max_post)):
        if db[i] > base + 4:
            end = max(end, i + 2)
        elif i > end:
            break
    return end


def text_between(words: list[dict], a: float, b: float) -> str:
    return " ".join(w["word"] for w in words if a <= w["start"] < b).strip()


def classify(sig: dict[str, np.ndarray], peak: int, text: str) -> tuple[str, list[str]]:
    w = slice(max(0, peak - 3), peak + 4)
    g = lambda k: float(np.max(sig[k][w])) if k in sig and len(sig[k]) else 0.0  # noqa: E731
    reasons = []
    for k, label in [("chat_velocity", "chat spike"), ("chat_hype", "chat hype words"),
                     ("heatmap", "most replayed"), ("loudness", "loud reaction"),
                     ("onset", "sudden scream/jump"), ("speech_hype", "hype words"),
                     ("scenes", "fast action")]:
        v = g(k)
        if v > 0.35:
            reasons.append(f"{label} ({v:.2f})")
    laugh, confused = g("chat_laugh_frac"), g("chat_confused_frac")
    t = text.lower()
    if laugh > 0.35 or re.search(r"\bha(ha)+|lmao|i'?m dying", t):
        arch = "funny"
    elif g("onset") > 0.5 and (SCARE_RX.search(t) or g("loudness") > 0.6) and not RAGE_RX.search(t):
        arch = "scare"
    elif RAGE_RX.search(t) and g("loudness") > 0.4:
        arch = "rage"
    elif CLUTCH_RX.search(t):
        arch = "clutch"
    elif confused > 0.35 or re.search(r"\bwhat (just|was|is)\b|how did", t):
        arch = "wtf"
    elif g("loudness") < 0.25 and g("speech_rate") > 0.3:
        arch = "story"
    else:
        arch = "hype"
    return arch, reasons


def pick_quote(segments: list[dict], peak: float, sig_hype: np.ndarray | None) -> str:
    """The most explosive short line near the peak, for the hook text.
    Stays inside one sentence so the quote reads naturally."""
    def hype_at(w):
        i = int(w["start"])
        return float(sig_hype[i]) if sig_hype is not None and i < len(sig_hype) else 0.0

    best, best_s = "", -1.0
    for seg in segments:
        if seg["end"] < peak - 6 or seg["start"] > peak + 4:
            continue
        ws = [w for w in seg.get("words", []) if w["word"].strip()]
        for i in range(len(ws)):
            for L in (3, 4, 5, 6, 7):
                chunk = ws[i:i + L]
                if len(chunk) < min(3, len(ws)):
                    continue
                s = sum(hype_at(c) for c in chunk) / len(chunk) * 3
                s += sum(c["word"].endswith(("!", "?")) for c in chunk) * 0.5
                s += 0.3 if i == 0 else 0  # starts a sentence
                s -= abs(chunk[0]["start"] - peak) * 0.05
                if s > best_s:
                    best, best_s = " ".join(c["word"] for c in chunk), s
    return best.strip(" ,.")


def make_hook(arch: str, quote: str, idx: int) -> str:
    """Use the streamer's own words when they're short and punchy, otherwise a
    template for the clip type (rotated so 25 clips don't share one hook)."""
    words = quote.split()
    if 3 <= len(words) <= 7 and len(quote) <= 38 and (
            any(ch in quote for ch in "!?") or idx % 2 == 0):
        return f'"{quote.upper()}"'
    opts = HOOK_TEMPLATES.get(arch, HOOK_TEMPLATES["hype"])
    return opts[idx % len(opts)]


def detect(sig: dict[str, np.ndarray], transcript: dict | None, words: list[dict],
           duration: float, count: int = 25, min_len: float = 15, max_len: float = 60,
           weights: dict | None = None, pool_factor: float = 2.0) -> tuple[list[Clip], np.ndarray]:
    weights = weights or DEFAULT_WEIGHTS
    n = int(duration)
    score = combine({k: v for k, v in sig.items() if k in weights}, weights)
    segs = _segments(transcript)
    db = sig.get("db")

    # pool of peaks: more than we need so overlap removal still leaves `count`
    min_gap = int(max(12, min(40, duration / max(count * 3, 1))))
    peaks = find_peaks(score, min_gap, int(count * pool_factor) + 10)

    clips: list[Clip] = []
    for p in peaks:
        rough = text_between(words, p - 10, p + 6)
        arch, reasons = classify(sig, p, rough)
        pre, post = ARCHETYPE_TIMING[arch]
        start = max(0.0, p - pre)
        end = float(reaction_end(db, p, post))
        start, end = snap_start(start, segs), snap_end(end, segs)
        if end - start < min_len:  # grow mostly backwards: more setup
            need = min_len - (end - start)
            start = max(0.0, start - need * 0.7)
            end = min(duration, end + need * 0.3)
            if end - start < min_len:
                start = max(0.0, end - min_len)
        if end - start > max_len:
            start = end - max_len
        end = min(end, duration)
        seg_score = float(np.mean(score[int(start):max(int(start) + 1, int(end))]))
        peak_score = float(score[p])
        clips.append(Clip(
            start=round(start, 2), end=round(end, 2), peak=float(p),
            score=round(0.75 * peak_score + 0.25 * seg_score, 4), archetype=arch,
            reasons=reasons, transcript=text_between(words, start, end),
            signals={k: round(float(v[p]), 3) for k, v in sig.items()
                     if k != "db" and len(v) > p}))

    clips = dedupe(clips)
    clips.sort(key=lambda c: c.score, reverse=True)
    for i, c in enumerate(clips):
        c.quote = pick_quote(segs, c.peak, sig.get("speech_hype"))
        c.hook = make_hook(c.archetype, c.quote, i)
    return clips, score


def dedupe(clips: list[Clip], max_overlap: float = 0.3) -> list[Clip]:
    kept: list[Clip] = []
    for c in sorted(clips, key=lambda c: c.score, reverse=True):
        ok = True
        for k in kept:
            ov = max(0.0, min(c.end, k.end) - max(c.start, k.start))
            if ov / max(1e-6, min(c.duration, k.duration)) > max_overlap:
                ok = False
                break
        if ok:
            kept.append(c)
    return kept
