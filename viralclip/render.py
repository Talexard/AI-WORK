"""Cut and render vertical 9:16 clips with word-by-word captions and a hook."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from .detect import Clip

W, H = 1080, 1920

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{font},92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,2,60,60,{cap_margin},1
Style: Hook,{font},70,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,18,0,8,80,80,{hook_margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

HIGHLIGHT = r"{\c&H00F0FF&\fscx112\fscy112}"  # yellow + slight pop (BGR)
RESET = r"{\c&HFFFFFF&\fscx100\fscy100}"


def _ts(t: float) -> str:
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def _esc(s: str) -> str:
    return s.replace("\\", "").replace("{", "(").replace("}", ")").replace("\n", " ")


def chunk_words(words: list[dict], max_words: int = 3, max_chars: int = 16) -> list[list[dict]]:
    chunks, cur = [], []
    for w in words:
        txt = w["word"].strip()
        if not txt:
            continue
        gap = (w["start"] - cur[-1]["end"]) if cur else 0
        if cur and (len(cur) >= max_words or gap > 0.6 or
                    len(" ".join(x["word"] for x in cur) + " " + txt) > max_chars or
                    cur[-1]["word"].endswith((".", "!", "?", ","))):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    return chunks


def build_ass(clip: Clip, words: list[dict], font: str, cap_margin: int,
              hook_margin: int, hook_secs: float = 3.0) -> str:
    out = [ASS_HEADER.format(W=W, H=H, font=font, cap_margin=cap_margin,
                             hook_margin=hook_margin)]
    if clip.hook:
        out.append(f"Dialogue: 1,{_ts(0)},{_ts(hook_secs)},Hook,,0,0,0,,"
                   f"{{\\fad(0,250)}}{_esc(clip.hook)}")
    inside = [w for w in words if clip.start <= w["start"] < clip.end]
    for ch in chunk_words(inside):
        toks = [_esc(w["word"]).upper() for w in ch]
        for j, w in enumerate(ch):
            a = w["start"] - clip.start
            b = (ch[j + 1]["start"] if j + 1 < len(ch) else max(w["end"], w["start"] + 0.25)) - clip.start
            line = " ".join((HIGHLIGHT + t + RESET) if k == j else t for k, t in enumerate(toks))
            out.append(f"Dialogue: 0,{_ts(a)},{_ts(min(b, clip.duration))},Cap,,0,0,0,,{line}")
    return "\n".join(out) + "\n"


def _even(x: float) -> int:
    return int(round(x / 2) * 2)


def video_filter(layout: str, zoom: float, facecam: tuple[float, float, float, float] | None) -> tuple[str, int, int]:
    """Returns (filter_complex producing [v], caption margin, hook margin)."""
    if layout == "crop":
        return (f"[0:v]scale=-2:{H},crop={W}:{H}[v]", 330, 160)
    if layout == "facecam" and facecam:
        x, y, w, h = facecam
        top_h, bot_h = 640, H - 640
        return (
            f"[0:v]split[f][g];"
            f"[f]crop=iw*{w}:ih*{h}:iw*{x}:ih*{y},scale={W}:{top_h}:force_original_aspect_ratio=increase,"
            f"crop={W}:{top_h}[top];"
            f"[g]scale=-2:{bot_h},crop={W}:{bot_h}[bot];"
            f"[top][bot]vstack[v]", 420, 560)
    # default: blurred fill + full gameplay in the middle (zoomed a little)
    fw = _even(W * zoom)
    return (
        f"[0:v]split[a][b];"
        f"[a]scale={W//4}:{H//4}:force_original_aspect_ratio=increase,crop={W//4}:{H//4},"
        f"boxblur=8:3,eq=brightness=-0.08,scale={W}:{H}[bg];"
        f"[b]scale={fw}:-2,crop={W}:ih[fg];"
        f"[bg][fg]overlay=0:(H-h)/2[v]", 300, 260)


def render(video: Path, clip: Clip, words: list[dict], out: Path, layout: str = "blur",
           zoom: float = 1.25, facecam=None, font: str = "Inter Display",
           captions: bool = True, crf: int = 20) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    vf, cap_m, hook_m = video_filter(layout, zoom, facecam)
    ass = out.with_suffix(".ass")
    ass.write_text(build_ass(clip, words if captions else [], font, cap_m, hook_m), encoding="utf-8")
    vf += f";[v]ass={ass.name},fps=30,format=yuv420p[vo]"
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{clip.start:.2f}", "-t", f"{clip.duration:.2f}",
           "-i", str(video.resolve()), "-filter_complex", vf, "-map", "[vo]", "-map", "0:a?",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", str(crf), "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
           "-movflags", "+faststart", out.name]
    subprocess.run(cmd, check=True, cwd=out.parent)
    return out


def slug(s: str, n: int = 40) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_-]+", "-", s)[:n].strip("-") or "clip"
