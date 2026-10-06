# Wan 2.7 — notes for Sabrina

## What it is on Higgsfield (`wan2_7`)
- Alibaba's video model; image-to-video with **native synced audio** and good character consistency.
- Inputs: `start_image`, `end_image`, `audio_references` (WAV/MP3). **No video reference** — it can't copy motion from a clip like Genjutsu.
- Duration 2–15 s; 720p or 1080p (no 480p); aspect 9:16, 16:9, 1:1, 4:3, 3:4.
- Supports free-trial unlimited generations when an allowance is active.

## Best uses for Sabrina
1. **Talking / lip-sync clips** — start_image = a Sabrina outfit image, audio_references = a voice line or song. Clean single-voice audio, no music, works best; audio longer than the clip gets trimmed.
2. **Bring a photo to life** — animate one of her outfit images or photo remakes (hair flip, turn, walk toward camera).
3. **Controlled transitions / loops** — start_image + end_image (e.g. outfit A → outfit B, or same frame for a loop).

## Prompting tips
- One main action + one clear scene per clip.
- State subject motion AND camera move ("she turns and smiles, slow push-in").
- Describe lighting, setting, mood, lens feel.
- Targeted negatives only: "no subtitles, no flicker, no distorted hands".

## When to use something else
- Copying a dance/motion from a clip → Genjutsu (`hf_mult_motion_control`).
- Need a video reference AND native audio → Wan 3.0 (`wan3_0`, takes video_references, 480p–1080p, up to 30 s).
