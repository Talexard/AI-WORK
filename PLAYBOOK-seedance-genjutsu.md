# Seedance 2.5 + Higgsfield Genjutsu Playbook

Our house rules for making AI video. Three rules come first:
1. **Every shot has to make sense.** One idea per shot, and nothing in the prompt should contradict anything else.
2. **The character fits the frame.** Nothing gets cut off by accident, and there's room to move.
3. **The lighting matches.** The character looks like they're really in the scene, not pasted in.

---

## 1. The tools

### Seedance 2.5 (ByteDance, released July 31, 2026)
- Up to **30 seconds in one continuous take** (no stitching)
- Up to **50 references** in a mix of images, video, audio and clay/3D renders
- Native audio (dialogue, sound effects, music)
- Modes: text-to-video, image-to-video, first-and-last-frame (keyframe), and region editing (re-render one area and leave the rest alone)
- **Resolution depends on the platform.** ByteDance advertises up to 4K, but **on Higgsfield it's 480p or 720p**. 8 seconds costs about 24 credits at 480p and 52 credits at 720p.
- **Save credits:** test at 480p and only render the final at 720p.

### Higgsfield Genjutsu (runs on Seedance)
It edits a video you already have instead of making a new one from scratch. There are two modes:
| Mode | What it does | Use it when |
|---|---|---|
| **Motion Transfer** | Takes the motion, camera move and timing from your clip and rebuilds the scene with a new character, location or look | "Same performance, different world/person" |
| **Object Swap** | Replaces one selected thing (character, outfit, product, object) and keeps everything else | "Same shot, just change X" |

- Source clip: **4–30 seconds**, MP4 or MOV. **10–15 seconds gives the best results.**
- Up to **30 reference images**
- Object Swap needs **at least 409,600 pixels per frame** (for example 854×480 or 640×640). Anything below that gets rejected.

---

## 2. Rule: the character fits the frame

### When filming the source clip for Genjutsu
- **One person, one continuous shot, steady camera.** No cuts, no zooms, and nobody walking through the frame.
- **Leave space around the subject:** room above the head, room on the side they face or move toward, and room for any gestures. If a hand or head leaves the frame in the source, the AI has to guess what it looks like.
- Film at the **final aspect ratio** (9:16 for Reels/TikTok, 16:9 for YouTube). Cropping later can cut off the new character.
- **Match the body type and proportions.** The new character takes the exact place of the original, at the same size and position. A tall, broad character swapped onto a small performer will look squashed or overflow the frame. Pick a performer whose build is close to the character's.
- If the character has big features like wings, a large coat, a tail or a helmet, **film wider** so there's room for them.
- Include in the prompt: *"Keep the lead's head and body the same apparent size and position in frame as the source."*

### When generating in Seedance
- Always give the **shot size**: wide, full body, medium, or close-up. "Full body, head to toe in frame, space above the head" stops feet and heads from getting cut off.
- **First and last frame:** both images must have the **same aspect ratio and resolution** and show the same location. Keep the character in a similar position in both, or the motion will warp.
- Use a first frame that's at least as big as the output (1920×1080 or more for 1080p).
- Use **one camera move per shot.** A pan, a dolly and an orbit together is how characters end up drifting out of frame.

---

## 3. Rule: the lighting matches

This is the most important rule. Mismatched lighting is the #1 sign of a fake composite. Check these **4 things** on every render:

| Check | What to look for |
|---|---|
| **Shadow direction** | The character's shadows fall the same way as the shadows in the scene |
| **Shadow softness** | Soft window light means soft shadows. Hard sun means hard shadows. They can't be mixed. |
| **Highlights** | The bright side of the face is the side facing the light source in the scene |
| **Color temperature** | A cool-lit character in a warm scene looks like a sticker. Match warm with warm and cool with cool. |

### How to get it right
1. **Light the source footage evenly and brightly.** Use a window in front of the subject or a ring light. Dark rooms and motion blur are where swaps break down.
2. **Reference images need the same lighting as each other.** Shoot the character's angles (front, three-quarter, side, back) under the same light. If the references disagree on lighting, the output will flicker between them.
3. **Describe the scene's light in the prompt,** in this order: **where it comes from → direction → hardness → color → the shadow it casts.**
   > *"Warm late-afternoon sun from camera left, hard light, long shadows falling to the right across the floor; the character is lit by the same sun with warm rim light on the left cheek."*
4. **Give the light a real source in the scene.** Name it: a window, a neon sign, a streetlight, a campfire. Motivated light looks real. Unexplained light looks pasted on.
5. **Tell it not to relight the scene.** For Object Swap: *"Keep the existing lighting direction and shadows of the scene; light the new character to match."*
6. **One lighting setup per shot.** Never ask for "soft natural light" and "hard neon contrast" in the same moment.
7. **Include contact shadows.** Feet on the ground and hands on objects should cast shadows. If they don't, the character looks like they're floating.

---

## 4. Rule: every shot makes sense

- **Prompt order for Seedance:** format → subject → action → setting → camera → look/lighting → timing → audio → constraints
- **Give the shot a beginning, middle and end.** For clips longer than 8 seconds, use timestamps:
  `0–8s: … | 8–18s: … | 18–30s: …`
  Don't write a great first 5 seconds and leave the rest undefined.
- **Cut conflicting words.** "Elegant, gritty, dreamy, glossy" gives the model four different directions. Pick one look.
- **Label every reference in the prompt:** `@Image1` = character front, `@Image2` = character profile, `@Image3` = location, `@Video1` = motion.
- **Image-to-video:** only describe the **motion**. Don't repeat what's already visible in the image.
- **Don't request things that contradict each other.** "Locked tripod" and "handheld" can't go together. "One continuous take" and "five cuts" can't go together.
- **Check that the physics hold up:** objects keep their size, hands hold things correctly, and the character stays on the ground.

---

## 5. Prompt templates

### Seedance 2.5: text/image-to-video
```
[FORMAT] 9:16 vertical, 15s, single continuous take, 720p.
[SUBJECT] @Image1 (front) / @Image2 (profile): <character>, <wardrobe>.
[ACTION] <what they do>.
[SETTING] @Image3: <location>, <time of day>.
[CAMERA] Medium-full shot, full body in frame with headroom, eye level, slow dolly-in. One move only.
[LIGHTING] <source> from <direction>, <hard/soft>, <color temp>; shadows fall <direction>;
           character lit by the same source, contact shadows on the ground.
[TIMING] 0–5s: … | 5–10s: … | 10–15s: …
[AUDIO] <ambience / dialogue / music>.
[CONSTRAINTS] Keep face, outfit and proportions consistent; character never leaves frame.
```

### Genjutsu: Motion Transfer
```
Keep the original motion, timing, camera angle, camera movement, framing and performance
from the uploaded video. Recast the main character using @Image1 and @Image2 (same person,
different angles). Move the scene to the location in @Image3. Keep the lead's head and body
the same apparent size and position in frame as the source. Light the character with the
location's light: <source, direction, softness, color>; shadows fall <direction>.
Add no new camera moves.
```

### Genjutsu: Object Swap
```
Replace only the selected character with the reference person in @Image1/@Image2.
Preserve the original background, other people, camera movement, timing, pose and
interaction. Keep the existing lighting direction and shadows of the scene and light
the new character to match. Keep the new character consistent across the full shot.
```

---

## 6. Pre-flight checklist (before spending credits)

**Source clip (Genjutsu)**
- [ ] 10–15 seconds, one continuous shot, steady camera, no zooms or cuts
- [ ] Only the subject in frame, with space around them
- [ ] Even, bright lighting and no motion blur
- [ ] Filmed at the final aspect ratio
- [ ] At least 854×480 (needed for Object Swap)
- [ ] Performer's build is close to the target character's

**References**
- [ ] Clean, well-lit images, each showing one main subject
- [ ] Character shown from several angles, all under the same lighting
- [ ] Wide establishing image of the location if it needs to be rebuilt
- [ ] Every reference is labeled in the prompt

**Prompt**
- [ ] Shot size stated, with "full body in frame" or headroom where needed
- [ ] One camera move
- [ ] Lighting described: source, direction, softness, color, shadows
- [ ] "Keep existing lighting and shadows" included for swaps
- [ ] No conflicting words or instructions
- [ ] Beginning, middle and end (timestamps if longer than 8 seconds)

**Review the 480p test before rendering the 720p final**
- [ ] Nothing gets cut off anywhere in the clip
- [ ] Shadows match in direction and softness
- [ ] Highlights are on the correct side
- [ ] Color temperature matches the scene
- [ ] Contact shadows present, no floating
- [ ] Face, outfit and proportions stay the same from start to end

---

## Sources
- [Higgsfield Genjutsu](https://higgsfield.ai/genjutsu) · [Meet Genjutsu](https://higgsfield.ai/blog/higgsfield-genjutsu)
- [Seedance 2.5 Prompting Guide (Higgsfield)](https://higgsfield.ai/blog/seedance-2-5-prompting-guide) · [Seedance 2.5 pricing on Higgsfield](https://higgsfield.ai/blog/seedance-2-5-pricing-2026)
- [Introducing Seedance 2.5 (ByteDance)](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)
- [Picsart: 30-second takes](https://picsart.com/blog/seedance-2-5-prompting-guide/) · [OpenArt prompt guide](https://openart.ai/blog/seedance-2-5-prompt-guide/) · [Atlas Cloud camera control](https://www.atlascloud.ai/blog/tips/seedance-2.5-camera-control-guide)
- [MindStudio: 50-reference system](https://www.mindstudio.ai/blog/seedance-2-5-multimodal-reference-system-explained)
- [Runway: Creating with Seedance 2.5](https://help.runwayml.com/hc/en-us/articles/53542207042323-Creating-with-Seedance-2-5) · [Seedance first/last frame](https://www.seedance.tv/blog/seedance-first-and-last-frame)
- [The Rundown: swap any video subject](https://app.therundown.ai/guides/swap-the-product-and-keep-the-performance-with-higgsfield) · [Willbastech Genjutsu tutorial](https://willbastech.com/blogs/news/higgsfield-genjutsu-ai-motion-swap-tutorial) · [Rekreate: limits & pricing](https://rekreate.ai/news/higgsfield-genjutsu)
- [OpenArt: match lighting](https://openart.ai/blog/match-lighting-in-ai-image-inpainting/) · [Akool: lighting & color matching](https://akool.com/knowledge-base-article/lighting-and-color-matching-in-background-changes)
- Tutorials found (not watched): [Genjutsu demo](https://www.youtube.com/watch?v=mDofSLaCWqw) · [Motion Transfer & Object Swap](https://www.youtube.com/watch?v=j1tFM5hnxfw) · [Seedance 2.5 in 20 min](https://www.youtube.com/watch?v=UxwV16jDglA)
