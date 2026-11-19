# viralclip

Give it a YouTube video or stream VOD. It finds the 20–30 moments most likely to go viral and renders each one as a ready-to-post 9:16 clip with word-by-word captions and a hook.

**Read first:** [`docs/VIRAL_CLIPS_PLAYBOOK.md`](docs/VIRAL_CLIPS_PLAYBOOK.md) covers what makes gaming clips go viral, the clip types that win, the anatomy of a clip second by second, and posting strategy. The tool is that playbook turned into code.

## How it finds moments

| Signal | Source | Catches |
|---|---|---|
| Chat velocity + hype words (`LMAO`, `💀`, `CLIP IT`, `????`) | YouTube live-chat replay (auto), Twitch chat JSON, or CSV | What the live audience reacted to |
| "Most Replayed" heatmap | YouTube metadata (auto) | What viewers rewound |
| Loudness spikes + sudden jumps | Audio | Screams, rage, jump scares |
| Hype speech ("no way", "oh my god", swearing, "let's go") | Whisper transcript | Big verbal reactions |
| Scene-cut density (`--scenes`) | Video | Fast action |

The signals are combined into a per-second score (with a bonus when several agree). The tool then picks the peaks and builds a window around each one: setup before the peak, the reaction after, both snapped to sentence boundaries, 15–60s long. It removes overlapping clips, sorts each one into a type (rage, clutch, funny, scare, WTF, story, hype) and writes a hook.
With `--ai`, Claude Opus 5.5 then judges each candidate like a human editor would. It re-ranks them, tightens the cuts, and writes the hooks, titles and hashtags.

## Install (on your own computer)

YouTube blocks most cloud/server IPs, so run this locally.

```bash
# needs ffmpeg installed (brew install ffmpeg / apt install ffmpeg / winget install ffmpeg)
pip install -r requirements.txt
```

## Use

```bash
# A YouTube video or past livestream: 25 clips (the default)
python -m viralclip "https://www.youtube.com/watch?v=VIDEO_ID" -o my_clips

# 30 clips, with Claude re-ranking and writing the hooks (needs ANTHROPIC_API_KEY)
python -m viralclip "URL" -n 30 --ai --game "Valorant"

# Facecam stacked on top of the gameplay. --facecam = x,y,w,h as fractions of the frame
# (example: a facecam in the bottom-right corner)
python -m viralclip "URL" --layout facecam --facecam 0.72,0.68,0.27,0.30

# A local Twitch VOD with chat exported by TwitchDownloader
python -m viralclip vod.mp4 --chat chat.json

# Preview the picks without rendering anything
python -m viralclip "URL" --dry-run
```

If YouTube says "Sign in to confirm you're not a bot", add `--cookies-from-browser chrome` (or firefox, edge).

### Output (`-o` folder)
- `01_rage_he-completely-lost-it.mp4`, … : ranked 1080×1920 clips with captions, the hook and normalised loudness
- `clips.csv` / `clips.json` : timestamps, score, clip type, hook, why it was picked, and a YouTube link to each moment (plus title and hashtags with `--ai`)

### Useful options
| Flag | Default | |
|---|---|---|
| `-n/--count` | 25 | number of clips |
| `--min-len/--max-len` | 15/60 | clip length in seconds |
| `--layout` | blur | `blur` (gameplay over a blurred fill), `crop` (centre crop), `facecam` |
| `--whisper-model` | small | `medium`/`large-v3` are more accurate; `tiny` is faster |
| `--chat-lag` | 6 | how many seconds chat trails the moment |
| `--weights` | | e.g. `'{"loudness":0.35,"chat_velocity":0.1}'` to tune for your streamer |
| `--no-captions`, `--scenes`, `--font` | | |

## Notes
- Short or calm videos don't contain 20–30 real moments. The tool warns you when it has to pad with weaker clips; post the top-ranked ones first.
- Only clip content you own or have permission to use, and credit the creator.
