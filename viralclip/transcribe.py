"""Word-level transcription with faster-whisper (local, free)."""
from __future__ import annotations

import json
from pathlib import Path


def transcribe(video: Path, out_json: Path, model_size: str = "small",
               language: str | None = None, device: str = "auto") -> dict:
    """Returns {"segments": [{start,end,text,words:[{start,end,word}]}]}.
    Cached to out_json so reruns are instant."""
    if out_json.exists():
        return json.loads(out_json.read_text())
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:  # pragma: no cover
        raise SystemExit("pip install faster-whisper  (or run with --no-transcribe)") from e

    compute = "int8"
    model = WhisperModel(model_size, device=device, compute_type=compute)
    segments, _info = model.transcribe(
        str(video), language=language, word_timestamps=True, vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 400})
    data = {"segments": []}
    for s in segments:
        data["segments"].append({
            "start": s.start, "end": s.end, "text": s.text.strip(),
            "words": [{"start": w.start, "end": w.end, "word": w.word.strip()}
                      for w in (s.words or [])],
        })
        print(f"\r  transcribed {s.end/60:6.1f} min", end="", flush=True)
    print()
    out_json.write_text(json.dumps(data))
    return data


def all_words(transcript: dict) -> list[dict]:
    return [w for s in transcript.get("segments", []) for w in s.get("words", [])]
