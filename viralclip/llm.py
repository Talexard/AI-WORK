"""Optional: have Claude judge candidates like a human clip editor.

Signals find *where* something happened; a model reading the transcript can
tell whether a stranger would understand and share it, tighten the
start/end, and write a better hook. Needs ANTHROPIC_API_KEY (or `ant auth login`)."""
from __future__ import annotations

import json

from .detect import Clip

MODEL = "claude-opus-5-5"

SYSTEM = """You are a top short-form editor who runs viral gaming clip channels \
(TikTok, YouTube Shorts, Reels). You know what gets shared: big readable \
reactions (rage, screams, laughter), clutch/insane plays, funny fails, jump \
scares, WTF glitches, drama/interactions, hot takes. A clip wins if a stranger \
who never saw the stream understands it in under 3 seconds and wants to send it \
to a friend. Clips must open on action or a strong line, never on filler, and \
end hard on the reaction so they loop."""

SCHEMA = {
    "type": "object",
    "properties": {
        "clips": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "virality": {"type": "integer", "description": "1-10"},
                    "archetype": {"type": "string",
                                  "enum": ["rage", "clutch", "funny", "scare", "wtf",
                                           "story", "hype", "wholesome", "drama",
                                           "fail", "first_look"]},
                    "start_offset": {"type": "number",
                                     "description": "seconds to move start (negative=earlier), -10..10"},
                    "end_offset": {"type": "number", "description": "seconds to move end, -10..10"},
                    "hook": {"type": "string", "description": "on-screen hook, <= 40 chars, may use 1 emoji"},
                    "title": {"type": "string", "description": "post title/caption, <= 90 chars"},
                    "hashtags": {"type": "array", "items": {"type": "string"}},
                    "why": {"type": "string", "description": "one sentence"},
                },
                "required": ["id", "virality", "archetype", "start_offset", "end_offset",
                             "hook", "title", "hashtags", "why"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["clips"],
    "additionalProperties": False,
}


def rerank(clips: list[Clip], video_title: str, creator: str = "",
           game_hint: str = "", effort: str = "medium", notes: str = "") -> list[Clip]:
    import anthropic

    client = anthropic.Anthropic()
    lines = []
    for i, c in enumerate(clips):
        lines.append(json.dumps({
            "id": i, "start": c.start, "end": c.end, "peak_at": c.peak,
            "detected_type": c.archetype, "signal_score": c.score,
            "signals": c.reasons, "transcript": c.transcript[:1500],
        }, ensure_ascii=False))
    prompt = (
        f"Video: {video_title!r}" + (f" by {creator}" if creator else "") +
        (f"\nGame: {game_hint}" if game_hint else "") +
        (f"\n\nWhat to look for with this creator/game:\n{notes}" if notes else "") +
        "\n\nBelow are candidate clips found by audio/chat/replay signals. "
        "Score EVERY candidate's virality 1-10 (be harsh: 8+ means it could "
        "realistically do 100k+ views), suggest start/end trims so it opens on "
        "the hook and ends on the reaction, and write the on-screen hook, a post "
        "title and 3-5 hashtags (game-specific first).\n\n" + "\n".join(lines))

    resp = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
        output_config={"effort": effort,
                       "format": {"type": "json_schema", "schema": SCHEMA}},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if resp.stop_reason == "refusal":
        print("  Claude declined to rank these clips; keeping signal ranking.")
        return clips
    text = "".join(b.text for b in resp.content if b.type == "text")
    data = json.loads(text)
    for r in data["clips"]:
        i = r["id"]
        if not 0 <= i < len(clips):
            continue
        c = clips[i]
        c.llm = r
        c.start = round(max(0.0, c.start + max(-10, min(10, r["start_offset"]))), 2)
        c.end = round(max(c.start + 8, c.end + max(-10, min(10, r["end_offset"]))), 2)
        c.archetype = r["archetype"]
        c.hook = r["hook"]
        # blend: model judgement 70%, signal strength 30%
        c.score = round(0.7 * (r["virality"] / 10) + 0.3 * min(1.0, c.score), 4)
    clips.sort(key=lambda c: c.score, reverse=True)
    return clips
