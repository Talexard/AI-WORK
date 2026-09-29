# Seedance 2.5 + Genjutsu Playbook: Beginner to Advanced

This is the hands-on "how do I actually do it" guide. Every shot we make has to pass three rules:

1. **It makes sense.** The action, the place and the character belong together, and nothing happens that the viewer can't follow.
2. **The character fits the frame.** Nobody gets cut off at the head or feet, and there's room to move.
3. **The lighting matches.** The subject looks like it was filmed in that place, not pasted on top of it.

Related guides: [realism and lighting in depth](seedance-genjutsu-realism.md) · [going viral](going-viral-with-ai-content.md)

> Researched September 2026 from tutorials, official docs and creator write-ups (list at the bottom). I couldn't play the videos themselves (the network here blocks YouTube), so this is built from their written guides, descriptions and write-ups. Some specs differ between sources and hosts, so where they conflict I note it. Always check the numbers in the app you're using.

---

# PART 1: SEEDANCE 2.5

## 1.1 What it is and what it can do

Seedance 2.5 is ByteDance's newest video model. It runs on Dreamina/CapCut, Higgsfield, Runway, fal, Morphic and other sites.

| Spec | Seedance 2.5 |
|---|---|
| Length | **4–30 s** per generation (2.0 is 4–15 s) |
| Resolution | **480p, 720p, 1080p** native (some hosts advertise 4K) |
| Aspect ratios | 16:9, **9:16**, and others |
| References | Up to **30 images, 10 videos, 10 audio** per generation |
| Modes | Text-to-video, image/reference-to-video, **Edit**, **Extend** (forward or backward) |
| Audio | Generates synced sound, voices and lip sync |

## 1.2 BEGINNER: your first good clip

### Step by step

1. **Open Seedance 2.5** in your app (on Dreamina/CapCut, pick the Seedance 2.5 model).
2. **Set the format first**: **9:16** for TikTok, Reels or Shorts, and **5–10 s** to start. Short clips give fewer errors and are cheaper to retry.
3. **Test at 480p or 720p.** Only render 1080p once the shot is right.
4. **Upload 1–3 references** (a character photo, maybe a location). Each gets a tag: `@Image1`, `@Image2`…
5. **Write the prompt with the 6-part formula** (below).
6. **Generate 2–4 versions** and pick the best one.
7. **Check it against the checklist** at the end of this guide before using it.

### The beginner formula (6 parts)

Write it as sentences, in this order:

1. **Subject**: who it is, tied to a reference: "The man in @Image1"
2. **Action**: one clear main action: "walks to the window and opens the curtains"
3. **Scene**: "in a small apartment bedroom, early morning"
4. **Camera**: exactly **one** camera move: "medium shot, slow push-in"
5. **Lighting**: at least **one** clear lighting description: "soft warm sunrise light from the window on camera-left"
6. **Style and constraints**: "natural color, light film grain, consistent face from @Image1, no text"

**Length:** keep beginner prompts around **40–100 words**.

### Beginner example

```
The man in @Image1, wearing a grey hoodie, walks to the bedroom window and pulls the curtains open, then squints as light hits his face.
A small, messy apartment bedroom, early morning.
Medium shot, 9:16 vertical, camera slowly pushes in toward him.
Soft warm sunrise light pours in from the window on camera-left, lighting the left side of his face; the right side falls into soft shadow. Dust floats in the light beam.
Natural color, light film grain. Keep his face exactly as in @Image1, no drift. Sound: curtain rings sliding, birds outside, no music.
```

### Beginner mistakes (and fixes)

| Mistake | What happens | Fix |
|---|---|---|
| Prompt too short ("a man in a room") | Random, generic result | Use all 6 parts |
| Buzzwords ("stunning, 8K, photorealistic") | Does nothing | Concrete words: "soft rim light," "handheld tracking shot," "shallow depth of field" |
| Too many actions in one short clip | Warping, morphing chaos | **One main action per clip** |
| Two camera moves that clash ("locked tripod" + "fast drone pan") | The scene splits and falls apart | **One camera command per clip** |
| Not saying what each reference is for | The model guesses wrong | "@Image1 is the character, @Image2 is the location" |
| Trying to get the whole video in one shot | Weak, messy result | Build the video from several clips (Part 1.3) |
| Character photo and location lit differently | Lighting looks "in between," fake | See Part 4 (lighting) |

## 1.3 ADVANCED: control like a director

### A. The full formula (for longer and multi-shot clips)

```
FORMAT      → 9:16, 20 seconds, 1080p look, handheld documentary style
SUBJECT     → who and what, locked to references
REFERENCES  → what EACH @ file does
TIMELINE    → Shot 1 / Shot 2 / ... with seconds
CAMERA      → one intention per shot
CONTINUITY  → what must stay the same across shots
AUDIO       → specific sound sources, near/far, "no music"
CONSTRAINTS → no text, no extra people, no face drift
```

### B. Multi-shot with timing

Seedance 2.5 cuts between shots when you label them `Shot 1:`, `Shot 2:`… **Give every shot its length in seconds.**

```
@Image1 is the main character (face, hair, jacket). @Image2 is the diner location. Keep both exactly the same in every shot.
Global: 9:16, 18 seconds, late-night diner, cold fluorescent overhead light mixed with red neon from the window sign. Handheld, 35mm look, light grain.

Shot 1, 6 seconds: Wide shot. The woman from @Image1 pushes the diner door open and walks toward the counter. Camera stays by the door. Red neon from the window paints her right side.
Shot 2, 6 seconds: Medium shot from behind the counter. She sits on a stool and slides a folded note across the counter. Overhead fluorescent light from above, soft shadows under her eyes, red neon rim on her right shoulder.
Shot 3, 6 seconds: Close-up of the note as a hand unfolds it; it reads nothing visible. Same fluorescent-plus-neon lighting.

Continuity: same jacket, same hair, same lighting setup in every shot. Her position in Shot 2 matches where she walked in Shot 1.
Audio: door chime near, fridge hum far, stool creak near, no music.
Constraints: no text on screen, no extra customers, no face drift.
```

### C. Timestamp blocks (several things in ONE shot)

When the order of events inside one continuous shot matters:

```
0–3 s: he picks up the phone and looks at the screen.
3–6 s: his expression drops; he slowly lowers the phone.
6–8 s: he turns and looks out of the window.
```

For each block, give a **camera intention, a visible action, a sound, a continuity note and an end state** (where things stand when the block ends).

### D. Reference roles: tell each file its job

```
@Image1 → character identity (face, hair, build)
@Image2 → outfit
@Image3 → location
@Video1 → camera movement ONLY (not the people or place)
@Audio1 → rhythm and pacing
```

- Start with **3–5 references**, each with one job. More references dilute each one.
- "Follow the camera movement of @Video1" works better than just mentioning `@Video1`.

### E. Edit mode: fix a part without redoing the whole clip

Seedance 2.5 can **rewrite only a region** of an existing video and keep the camera motion, lighting direction and composition. On Dreamina you can **mark the area** and describe the change.

- Trigger words: **edit, remove, add, replace, change to, restyle, relight**.
- Always add what to **keep**:

```
Replace the coffee cup on the table with the product from @Image1.
Keep the original lighting direction, camera angle, composition, the woman's motion and the audio timing unchanged.
The new product sits on the table with a soft contact shadow matching the other objects, lit by the same window light from camera-right.
```

- **Relight example** (matching a new background):

```
Keep the presenter, her outfit, performance and gestures exactly the same. Replace the backdrop with a bright modern office. Subtly relight her edges with cool daylight from the new office windows behind her so she matches the brighter environment.
```

Edit and Extend always keep **the source video's aspect ratio**. You can't change it there, so choose 9:16 or 16:9 before the first generation.

### F. Extend mode: longer videos that connect

- **Continue** starts from the source video's **last frame**. **Prepend** builds up to its **first frame**.
- New segments are 4–30 s each, at 480p/720p/1080p.
- Set the length to match the new content, and **only describe what happens next**.
- Manual version on any platform: **generate clip 1, save its last frame, use that frame as the reference for clip 2**, and describe only the new action with the same lighting words.

### G. Audio like a pro

- Name the sound sources and whether they're **near or far**: "footsteps near, traffic far."
- End with **"no music"** if you'll add music in the edit. Otherwise the model makes its own, and you can't cut it cleanly.
- Dialogue goes in "double quotes" and gets lip-synced.

---

# PART 2: GENJUTSU (Higgsfield)

## 2.1 What it is and what it can do

Genjutsu turns **video you already have** into something new. It keeps the motion and changes the look.

| | |
|---|---|
| **Motion Transfer** | Keeps the motion, camera and timing and rebuilds **everything else** (person, place, style) from your references |
| **Object Swap** | Changes **one selected thing** (person, outfit, product, object, location) and keeps the rest of the shot, including **your room, your light and your camera** |
| Source video | About **4–30 s** (some sources say 3 s minimum). **10–15 s works best** |
| Reference images | Up to **30–40** (sources differ) |
| Output | Up to **1080p** |
| Presets | **30+ presets** that can do the whole job, with an optional short description |
| Cost (15 s) | About **40 credits at 480p, 104 at 720p, 144 at 1080p** |

## 2.2 BEGINNER: your first swap

### Step by step

1. **Film your source clip** (rules below). Keep it 10–15 s, with one person, one shot and a steady camera.
2. **Open Genjutsu** on Higgsfield and **choose the mode**:
   - Want to become a character but **keep your room and light**? Use **Object Swap**.
   - Want a **new place, new look, new everything** but the same movement? Use **Motion Transfer**.
3. **Upload the source video.**
4. **Upload reference images** of the new character, outfit, product or place.
5. **Pick a preset** *or* write a short description. Simple object swap wording:
   > Replace [the person / the object in the source video] with [the character / object in the reference image]. Keep the rest of the shot the same.
6. **Generate at 480p** first (cheap), compare it with the source, and fix anything wrong.
7. **Render the final at 1080p.**

### How to film a source clip that works

- **One person, one continuous shot.** No cuts, no zooms, no one walking in front.
- **Steady camera**: tripod, or leaned against something. Heavy shake = failed swaps.
- **Bright, even light.** Face a window or a ring light. **Dark rooms and motion blur make swaps fail.**
- **Slow, clear movement.** Fast hands smear and come back with wrong fingers.
- **Keep the whole body part you need in frame the entire time** (see Part 3).

### Reference images that work

- **Clear, front-facing, sharp face**, with even light and **no filters** or beauty mode.
- **Match the framing**: a close-up needs a tight portrait reference, and a wide shot needs a **full-body** reference.
- **Hands visible** in the reference if hands show in the video.
- **Pick a character with a similar build to yours.** Cleaner swaps (see Part 3 for why).
- For products: photos from **every angle** the product is seen from in the video.

## 2.3 ADVANCED

### A. "Protect, change, match" briefs

When presets aren't enough, write it in three blocks. **Protect first.**

```
PROTECT: all body motion, timing, camera path, shot size and framing from the source video. Lighting direction and color stay the same: warm lamp light from camera-right, dim blue window light from behind.
CHANGE: replace the performer with the character in the reference images (face, fur, build). Keep body proportions consistent through the whole clip.
MATCH: the character is lit by the same warm lamp from camera-right with a cool blue rim from the window. Keep contact shadows under the feet and hands. Keep the source's grain, sharpness and motion blur. The swap tracks perspective and shadows across the whole shot.
```

### B. Make yourself the reference pose

Take a **frame from your source video** (the clearest, front-facing, unblocked one, not necessarily the first). Then create your character reference image **in that same pose, facing the same direction, at the same size in frame and lit the same way** (for example with ChatGPT or another image generator). The closer the reference matches the video, the cleaner the swap.

### C. Consistent characters across a whole series

- Use **Higgsfield Soul ID** (trained once) to keep the same face across Seedance, Kling, Veo and more, or keep a fixed **reference pack** per character: front, 3/4 and full body, all evenly lit.
- Reuse the **same reference files and the same description words** every episode.

### D. Genjutsu + Seedance together

| Job | Tool |
|---|---|
| Hero shots with real acting (your performance) | **Genjutsu** |
| Establishing shots, B-roll, impossible shots | **Seedance 2.5** |
| Fixing one detail in any clip (a cup, a sign, a sleeve) | **Seedance 2.5 Edit** (region edit) |
| Making a clip longer | **Seedance 2.5 Extend** |
| Final finishing: grade, grain, sound | Your editor (CapCut, Premiere, Resolve) |

### E. Common problems

| Problem | Cause | Fix |
|---|---|---|
| Background drifts or light looks wrong | Wrong mode | **Object Swap** keeps your room and light. Motion Transfer rebuilds it |
| Face flickers | Weak face reference, long clip | Sharper front and 3/4 references, 10–15 s clips |
| Hands warp | Fast hands, hands leaving frame | Slower hands, keep them in frame |
| Feet float or slide | Feet cut off in the source | Film full body with feet visible, and ask for contact shadows |
| Character looks squished or stretched | Build too different from the performer | Pick a similar build, or shoot wider (Part 3) |
| Head or ears cut off | No headroom in the source | Reshoot with more space (Part 3) |

---

# PART 3: MAKING THE CHARACTER FIT THE FRAME

The AI **keeps your source framing**. If the frame is too tight in the source, it will be too tight in the result, only worse, because the new character may be **bigger** than you. **You fix framing when you film, not afterwards.**

### Rule 1: Leave space around the performer

In a 9:16 vertical frame:

```
┌──────────────────┐
│   TOP 12–15%     │ ← headroom. Taller characters, hats, ears and horns need MORE (20–25%)
│                  │
│   ┌──────────┐   │
│   │          │   │
│   │ PERFORMER│   │ ← body in the middle area, centered or on a third
│   │          │   │
│   │          │   │
│   └──────────┘   │
│   BOTTOM 8–10%   │ ← space below the feet (if feet are in the shot)
│  (app buttons +  │ ← keep key action out of the bottom ~20% and right ~15%:
│   captions here) │    TikTok/Reels buttons and captions cover it
└──────────────────┘
      ↔ 10% each side, more on the side the character moves toward
```

### Rule 2: Frame for the *new* character, not for you

- **Bigger character** (Bigfoot, a giant, a hero in armor, a character with wings): **step back or zoom out** so the performer fills only **about 50–60% of the frame height**. That leaves room for a taller head, wider shoulders or a tail.
- **Smaller character** (a child, an animal, a small creature): keep the framing tighter, or the character looks lost in empty space.
- **Similar build to you**: the cleanest swaps. Pick characters close to your size when you can.
- Hats, horns, ears, hair buns and big hairstyles all need **extra headroom**.

### Rule 3: Nothing important leaves the frame

- Every body part that moves (head, hands, feet, props) should **stay inside the frame for the whole clip**. When a hand leaves the frame and comes back, the AI has to "guess" it again, and that's where fingers go wrong.
- If you jump, spin or raise your arms, **test the move first** and film it wide enough.
- **Walking toward the camera?** You'll get bigger in frame, so start further back.

### Rule 4: Match shot size to the reference

| Shot | What's in frame | Reference image needed |
|---|---|---|
| Close-up | Face and shoulders | Tight portrait, sharp face |
| Medium | Waist up | Waist-up or 3/4 body |
| Wide | Full body with feet | **Full-body** reference, feet visible |

A wide shot asks the AI to **rebuild the whole body**, and a close-up only asks it to protect the face. Wide shots need the best full-body references.

### Rule 5: Camera height makes sense

- Camera at **chest or eye height** looks natural for most scenes.
- For a **giant** character: put the camera **lower**, looking up a little.
- For a **tiny** character: put the camera **low, near the ground**. Otherwise the character sits at the bottom of a mostly empty frame.
- The horizon and everything in the room should agree with that camera height.

### Rule 6: Seedance framing words

When Seedance creates the shot from scratch, say the framing clearly:

```
Full-body wide shot, 9:16 vertical. The character fills about 60% of the frame height, with clear headroom above and her feet fully visible with space below. She stays centered in frame the whole time; nothing is cropped.
```

---

# PART 4: LIGHTING THAT MATCHES (NO COPY-PASTE LOOK)

This is the most important part. The full method is in the [realism guide](seedance-genjutsu-realism.md#3-the-lighting-match-method). Here's how to apply it in each tool.

### The 5 questions (answer before every shot)

1. **Where does the main light come from?** (left, right, front, behind, above)
2. **Hard or soft?** (sharp shadow edges = hard sun; blurry shadows = cloudy or window light)
3. **What color?** (warm orange lamp or sunset / neutral daylight / cool blue night or screen)
4. **What colored things are near the subject?** (a red wall or green grass bounces color onto skin)
5. **Where do the shadows fall?** (the subject's shadow must fall the same way as everything else's)

### In Genjutsu

- **Your source clip's light IS the final light.** Want sunset in the result? Film at sunset. Want a spooky dark hallway? Film in a dim hallway, but with enough light on your face for the swap to work.
- **Object Swap keeps your real light.** It's the safest mode for matching.
- **Motion Transfer rebuilds the scene**, so describe the new light fully in the MATCH block, including shadows and the subject's light.
- **References should be evenly and softly lit.** A character photo with hard light going the wrong way fights your video. Neutral soft light is easiest for the AI to relight.

### In Seedance 2.5

- **Use the same lighting sentence in every shot of the same place.** Same words give the same light, which gives continuity.
- **Make references agree.** If your character photo has warm side light and your location has cold overhead light, the model splits the difference and both look wrong.
- **Describe the light on the subject AND the interaction**: the shadow on the ground, bounce color, rim light, reflections.
- **Fix a mismatch with Edit and `relight`** instead of regenerating the whole thing.

### Lighting lines you can copy

| Scene | Lighting line |
|---|---|
| Golden hour outdoors | Low warm sun behind the subject on camera-left, golden rim light on hair and shoulders, face in soft open shade with cool sky fill, long shadows falling toward camera-right |
| Indoor daytime window | Soft daylight from a large window on camera-left, gentle falloff into shadow on the right side of the face, catchlights in the eyes, soft contact shadows |
| Night street / neon | Pink neon from camera-right colors the right side of the face, cool blue streetlight rim from behind, wet ground reflects both colors, deep but not crushed shadows |
| Office / fluorescent | Flat cool overhead fluorescent light, soft shadows under the eyes and chin, slight green tint, even light across the room |
| Campfire / candle | Warm flickering orange light from below and in front, deep dark surroundings, light dancing on the face, shadows moving with the flame |
| Overcast outdoors | Soft even grey daylight from above, almost no hard shadows, soft contact shadows under feet, muted colors |

---

# PART 5: THE FINAL CHECKLIST (every clip)

**Makes sense**
- [ ] The action fits the place and the character (no random objects, no impossible physics unless that's the joke)
- [ ] The story is clear with the sound off
- [ ] The character looks the same from start to end (face, clothes, size)

**Fits the frame**
- [ ] Head, hats, ears and hair are never cut off; there's headroom
- [ ] Hands and feet stay in frame when they matter
- [ ] The character is the right size for the scene (not squished, not tiny in empty space)
- [ ] Key action stays out of the bottom ~20% and right edge (app buttons)
- [ ] Camera height makes sense for the character's size

**Lighting matches**
- [ ] Light hits the character from the same direction as the scene
- [ ] Same warmth or coolness as the scene
- [ ] Shadow softness matches (hard sun = hard shadows everywhere)
- [ ] The character's shadow falls the same way as everything else's, and the feet touch the ground
- [ ] Nearby colors tint the character (bounce)
- [ ] Grain and sharpness match the background

**Technical**
- [ ] No warped hands, flicker or melting edges (watch it frame by frame at least once)
- [ ] 9:16, 1080×1920 for short-form
- [ ] AI label turned on when posting

---

## Sources

**Seedance 2.5: official, docs and guides**
- [ByteDance Seed: Introducing Seedance 2.5](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)
- [BytePlus ModelArk: Dreamina Seedance 2.5 prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2607689)
- [Dreamina: Seedance 2.5 prompt guide](https://dreamina.capcut.com/seedance/seedance-2-5-prompt)
- [Dreamina: Seedance 2.5 localized editing](https://dreamina.capcut.com/seedance/seedance-2-5-localized-editing)
- [Dreamina: Edit video without changing lighting or composition](https://dreamina.capcut.com/ai-video/how-to-edit-video-without-changing-lighting-composition)
- [Runware: Editing video with Seedance 2.5](https://runware.ai/docs/models/bytedance-seedance-2-5/guides/editing)
- [Runway Help: Creating with Seedance 2.5](https://help.runwayml.com/hc/en-us/articles/53542207042323-Creating-with-Seedance-2-5)
- [Morphic: Seedance 2.5 prompts, 1080p, edit, extend](https://morphic.com/resources/how-to/seedance-2-5-guide)
- [Kapwing: How to prompt Seedance 2.5](https://www.kapwing.com/resources/how-to-prompt-seedance-2-5-a-guide-for-ai-video-creators/)
- [fal: Seedance 2.5 prompting guide](https://fal.ai/learn/devs/seedance-2-5-prompting-guide)
- [Segmind: Advanced Seedance 2.5 prompts, 5 expert patterns](https://blog.segmind.com/advanced-seedance-2-5-prompts-5-expert-patterns-tested-2026/)
- [Medium: Practical guide to 30-second prompts](https://medium.com/@mchfollow/how-to-use-seedance-2-5-c87cb4dc1d24)
- [Framia: Step-by-step beginner tutorial](https://framia.converge.ai/page/en-US/news/how-to-use-seedance-2-5)
- [Seedance troubleshooting and common mistakes](https://www.bigmotion.ai/user-guide/seedance-2-0-tips-troubleshooting)

**Seedance 2.5: video tutorials found** (I couldn't play these; the details come from their descriptions)
- [Edit Videos with Prompts and Marks](https://www.youtube.com/watch?v=ldwNEuRRPZc)
- [Seedance 2.0 and 2.5 Masterclass: Beginner to AI Filmmaker (playlist)](https://www.youtube.com/playlist?list=PLoknIOnpU4ocGZNW11oBsrfMVyJSUrPID)
- [Seedance 2.0 & 2.5 Tutorial (playlist)](https://www.youtube.com/playlist?list=PLIi08al-Zd_mNu9ZlAiwPDpw0FWAL3xoc)
- [Full Tutorial: Access on CapCut + build a teaser](https://www.youtube.com/watch?v=pw_Dzp2MVbE)
- [Master It in 12 Minutes](https://www.youtube.com/watch?v=FqZ1CqJZZIs)
- [Cinematic AI Video From Start to Finish](https://www.youtube.com/watch?v=H0Ahmz2xuvs)
- [My Full Cinematic AI Film Workflow](https://www.youtube.com/watch?v=MY6f9xnYOwU)
- [Dreamina Seedance 2.5 Smart Edit Tutorial](https://www.youtube.com/watch?v=CJdWOQNVJw8)

**Genjutsu**
- [Higgsfield Genjutsu](https://higgsfield.ai/genjutsu) · [Meet Higgsfield Genjutsu](https://higgsfield.ai/blog/higgsfield-genjutsu)
- [The Rundown: Swap any video subject with Higgsfield](https://app.therundown.ai/guides/swap-the-product-and-keep-the-performance-with-higgsfield)
- [Cindy Zhu: Turn yourself into anyone with ChatGPT and Genjutsu](https://cindyzhu.com.au/guides/turn-yourself-into-anyone-higgsfield-genjutsu)
- [Dreamina: Genjutsu-style workflow](https://dreamina.capcut.com/ai-video/higgsfield-ai-genjutsu)
- [Rekreate: Genjutsu limits and pricing](https://rekreate.ai/news/higgsfield-genjutsu)
- [Higgsfield: Soul ID character consistency](https://higgsfield.ai/blog/sould-id-best-character-consistency)
- Video tutorials (from their descriptions): [Video to Video Tutorial](https://www.youtube.com/watch?v=E0V0vSy4MRg) · [Motion Transfer & Object Swap Tutorial](https://www.youtube.com/watch?v=j1tFM5hnxfw) · [Genjutsu Demo](https://www.youtube.com/watch?v=mDofSLaCWqw) · [3 Simple Steps](https://www.youtube.com/shorts/5bPsPmr9FXw)

**Framing**
- [Scenario: AI video character replacement](https://www.scenario.com/blog/keep-shot-swap-character-p-video-replace-scenario)
- [Wikipedia: Headroom (photographic framing)](https://en.wikipedia.org/wiki/Headroom_(photographic_framing))
