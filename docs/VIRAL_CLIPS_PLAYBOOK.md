# Viral Gaming Clips: The Playbook

This covers what makes a clip from a gaming stream or YouTube video take off on TikTok, YouTube Shorts and Reels, and how `viralclip` turns that into code.

> A note on the numbers: platforms publish almost nothing official about ranking. The thresholds below come from creator-tool vendors and creator experience. Use them as rules of thumb and compare against your own analytics.

---

## 1. How the platforms decide

All three short-form feeds work roughly the same way:

1. **A seed test.** A new clip is shown to a small batch of viewers who already watch similar content (for example, people who watch Valorant or Minecraft clips).
2. **Measuring the first second.** The biggest early signal is whether people swipe away immediately. YouTube Studio shows this as **"Viewed vs. swiped away"**. Creators aim for 60–70%+ viewed.
3. **Retention and loops.** The clip keeps getting pushed if people watch most of it, and especially if they watch it again. Rewatching is the strongest "this is good" signal. A clip that ends right at the payoff often loops naturally.
4. **Shares and saves count more than likes.** "Sending this to the group chat" is the behaviour behind most gaming virality.
5. **Expansion.** If the seed batch does well, the clip goes to a wider audience. That's why a clip can sit at 300 views for two days and then jump to 2M.

**What that means for a clipper:** the first second has to grab, the middle has to hold, and the ending has to pay off fast. Nothing else matters as much.

---

## 2. The clip types that go viral (gaming)

Ranked roughly by how often they hit, across streamer and YouTuber clip channels:

| # | Type | What it looks like | Why it spreads |
|---|---|---|---|
| 1 | **Rage / scream** | The streamer loses it: yelling, slamming the desk, a meltdown after a death | Big emotion is readable without context; the sound alone stops the scroll |
| 2 | **Clutch / insane play** | A 1v4, an ace, a no-scope, a last-second win, a speedrun trick | Skill plus suspense, and gamers share it to argue about it |
| 3 | **Funny fail** | Falls off the map, team-kills, misses an easy shot, a bug launches them across the map | Schadenfreude, instantly understood, loops well |
| 4 | **Jump scare** | Horror games: a scream plus a cut to the facecam | Physical reaction; people watch it again to see the face |
| 5 | **WTF / glitch** | Physics bugs, cursed spawns, "how is that possible" | The comments section turns into a debate, which drives engagement |
| 6 | **Interaction / drama** | A troll in voice chat, a donation-message reaction, a clash with a duo partner, a celebrity cameo | Story plus personality; the clip channel's favourite |
| 7 | **Hot take / rant** | The streamer sounds off about a game, a patch, another creator | Divisive, so the comments fill up |
| 8 | **Wholesome** | A kid in voice chat, a surprise for a viewer, the community helping | Very high share rate, a lower ceiling |

**What all the winners share:** a big *reaction* tied to a clear *cause* that a stranger understands in under 3 seconds, without having seen the stream.

---

## 3. Anatomy of a viral clip (second by second)

```
0.0–1.5s  HOOK       Start mid-action or on the most intense line. Never start with "so, um".
                     A text hook on screen ("He did NOT see this coming 💀").
1.5–8s    SETUP      Just enough context to understand the stakes (1 HP, last round, a scary hallway).
8–25s     ESCALATION Build tension; the chat starts going crazy.
PEAK      PAYOFF     The kill, the scream, the punchline.
+1–4s     REACTION   The streamer's face or voice reacting. This is the part people share.
END       CUT HARD   End on the reaction. No outro. A hard cut makes it loop.
```

Rules that keep coming up:

- **Length.** 15–35s is the sweet spot for pure moments. Up to 60s works for stories or interactions *if* the tension builds the whole way.
- **Cut the dead air.** Remove pauses longer than about 0.7s, loading screens and menus.
- **Captions are not optional.** Most people scroll with the sound off. Use big, bold, high-contrast captions of 1–3 words at a time, centred in the lower-middle of the frame.
- **Vertical 9:16.** Either a facecam stacked on top of the gameplay, or the gameplay centred over a blurred fill. The face matters: reactions *are* the content.
- **Hook text.** One short line in the first ~3 seconds, framed as curiosity or stakes, never a plain description ("Gameplay part 3" ❌ → "He thought he was safe 😭" ✅).
- **Sound.** Keep the original audio. The scream *is* the hook, so normalise loudness and don't let it clip.
- **Titles and captions.** Name the game plus the emotion. 3–5 targeted hashtags (#valorant #valorantclips #gaming); hashtags matter much less than they used to.

---

## 4. Where to find viral moments in a long video (the signals)

People who clip by hand watch a 6-hour VOD at 2× speed and look for the same handful of things. Each of them can be measured:

| Signal | What it means | How we measure it |
|---|---|---|
| **Chat velocity spike** | The audience reacted *live*: the most reliable crowd-sourced signal there is | Messages per second compared with the stream's rolling baseline (z-score), **moved ~6s earlier** because chat lags behind the moment |
| **Chat hype words** | *How* the chat reacted: `LMAO`, `KEKW`, `💀`, `W`, `CLIP IT`, `?????`, `NO WAY` | A weighted count of hype tokens per second; the mix of tokens hints at the clip type (laughing = funny, `?` = WTF) |
| **YouTube "Most Replayed" heatmap** | Viewers *rewound* to this part of the VOD | yt-dlp exposes `heatmap` from the video's metadata |
| **Audio loudness spike** | Screaming, yelling, an explosion | RMS loudness in dB compared with the local baseline (a rolling 60s median), so a loud game doesn't flag everything |
| **Sudden loudness jump (onset)** | Jump scares, a rage burst, a sudden "WHAT" | dB rise from the 2s before to the 1s after |
| **Hype speech** | "oh my god", "no way", "let's go", "bro", swearing, "what" | Word-level transcript (Whisper) matched against a weighted phrase list |
| **Fast speech** | Panic or excitement | Words per second compared with the speaker's median |
| **Laughter or silence after a moment** | A punchline or shock | The loudness pattern after the peak |

`viralclip` combines whatever signals exist for a video (live-stream VODs have chat; normal uploads usually have a heatmap; everything has audio and speech) into one per-second **virality score**, then picks the peaks.

---

## 5. From peaks to clips

1. **Pick the peaks** on the smoothed score, with spacing between them so you don't get 5 clips of the same moment.
2. **Build the window** around each peak:
   - *Start:* about 8–20s before the peak (more setup for clutches and stories, less for screams), **snapped to the start of a sentence** so no clip opens mid-word.
   - *End:* 2–6s after the peak, once the reaction calms down (loudness back to baseline), snapped to the end of a sentence.
   - Keep the length between 15 and 60s.
3. **Remove overlaps.** If two windows overlap by more than about 30%, keep the higher score.
4. **Classify the clip type** (rage, clutch, funny, scare, WTF, story) from the mix of signals.
5. **Write a hook.** Use the most explosive quote near the peak, plus a template for that clip type.
6. **Optional AI pass:** send the top ~45 candidates' transcripts to Claude to judge them like a human editor ("would a stranger understand and share this?"), tighten the start and end, and write the hook text. Keep the best 20–30.
7. **Render:** 9:16, either a blurred fill or a facecam stack; word-by-word captions; the hook text for the first 3s; loudness normalisation.

### Why 20–30 per video works

A 2–4 hour stream usually has 30–60 moments worth reacting to. Posting 20–30 clips from it is a volume strategy: you can't know in advance which 1–2 will break out, so you post many good candidates and let the seed tests pick the winner. The quality bar still applies: 10 strong clips beat 50 mediocre ones on the same account. Spread them across days and platforms rather than dumping all 30 at once.

**Short videos (under 20 min) don't contain 20–30 good moments.** The tool tells you when it had to lower its threshold to reach the count you asked for.

---

## 6. Posting strategy

- Post 2–4 clips a day per platform, not all at once.
- Lead with the highest-scoring clip types (rage, clutch, funny).
- Put the same clip on TikTok, Shorts and Reels. Each platform's seed test is separate.
- After 48h, check viewed-vs-swiped and average % viewed. Rework the hook (the first second plus the text) on clips that got views but lost people early.
- Pull the winning *clip types* back into your weights (`--weights`) so the scorer learns what your audience shares.

## 7. Rights

Clip only content you own or have permission to use (many streamers run official clipping programmes, or allow clipping with credit or revenue share). Credit the creator in the caption. Reposting someone else's content without permission can get your account struck.

---

### Sources
- [Eklipse: optimising gaming clips for TikTok/Reels/Shorts](https://blog.eklipse.gg/de/clip-guide/gaming-clips-tiktok-reels-shorts-optimieren.html)
- [Medal: how to grow gaming content](https://medal.tv/learn/how-to-grow-gaming-content)
- [vidIQ: How the YouTube Shorts algorithm works in 2026](https://vidiq.com/blog/post/youtube-shorts-algorithm/)
- [OutlierKit: The Shorts algorithm in YouTube's words](https://outlierkit.com/resources/youtube-shorts-algorithm/)
- [Shortimize: Shorts retention rate](https://www.shortimize.com/blog/youtube-shorts-retention-rate)
- [Autoclip: 10 types of viral clip hooks](https://autoclip.dev/blog/10-types-of-viral-clip-hooks)
- [OpusClip: clip the moments your live chat exploded](https://www.opus.pro/mcp/inspiration/clip-the-moments-your-live-chat-exploded)
- [TechCrunch: Powder detects when a creator yells](https://techcrunch.com/2023/11/20/powder-an-ai-clipping-tool-for-gaming-can-detect-when-a-creator-yells-during-a-stream)
- [LIGHTOR (SFU): highlight detection from chat](https://www2.cs.sfu.ca/~jnwang/papers/lightor.pdf)
- [CTIC chat burst detector](https://github.com/josec07/clipper)
