# Making AI Video That Looks Real: Seedance + Genjutsu

A working guide to generating and editing AI video with **Seedance** (ByteDance's video model) and **Genjutsu** (Higgsfield's video-to-video tool), with one goal above everything else: **the result must look like it was filmed, not pasted together.**

> Specs and prices below were collected in September 2026 from public guides (sources at the bottom). These tools update often, so re-check limits in the app before a big job.

---

## 1. Which tool does what

| | **Seedance** | **Genjutsu** |
|---|---|---|
| What it is | Creates a new video from text, images, video and audio references | Edits a video you already have (video-to-video) |
| Starts from | A prompt plus optional references | Your real footage plus reference images |
| Use it when | You need a shot that doesn't exist yet | You already have the motion or camera move you want and need to change who, what or where |
| Where to run it | Dreamina/CapCut, Higgsfield, fal, BytePlus ModelArk and other hosts | Higgsfield |

**Simple rule:** if the **movement** is already right in real footage, use **Genjutsu**. If you need the whole shot invented, use **Seedance**. Many good pieces use both: Seedance for B-roll and establishing shots, Genjutsu for the hero shots built from real performances.

### Seedance versions

| | Seedance 2.0 | Seedance 2.5 |
|---|---|---|
| Length per generation | 4–15 s | 4–30 s |
| Resolution | 480p up to 4K | 480p / 720p |
| Max references | 12 (9 images, 3 videos, 3 audio) | 50 (30 images, 10 videos, 10 audio) |
| Pick it for | Final resolution, lower cost | Longer takes, multi-shot story beats, heavy referencing |

A practical pattern: **plan and test in 2.5** (long and cheap at 480p), then **render the finals in 2.0** at 1080p or 4K when a shot fits in 15 s.

### Genjutsu modes

- **Motion Transfer**: keeps the source clip's motion, camera and timing and **rebuilds everything else** (new person, new place, new look) from your references.
- **Object Swap**: changes **one selected thing** (character, outfit, product, location, object) and leaves the rest of the shot as it was.

Limits: source video **3–30 s**, up to **40 reference images**, output up to **1080p**. A 15 s clip costs about **40 credits at 480p, 104 at 720p and 144 at 1080p**. The app shows the cost before you run it.

---

## 2. Why AI video looks fake (the "copy and paste" problem)

People can't always say *why* a shot looks fake, but it almost always comes down to one of these. Learn to spot them, because every step later in this guide exists to prevent one.

1. **Light direction doesn't match.** Background sun comes from the left, but the subject's face is lit from the right.
2. **Color temperature doesn't match.** A warm (orange) subject in a cool (blue) scene, or the reverse.
3. **Light quality doesn't match.** Hard, crisp shadows on the subject, while the scene is overcast with soft shadows (or the reverse).
4. **No contact shadow.** Feet or objects don't darken the ground where they touch it, so they float.
5. **No bounce or spill.** In real life a green wall tints the side of a face green, and a red neon sign puts red on skin. Pasted subjects stay "clean."
6. **Black levels and contrast differ.** The subject's darkest shadows are deeper or more washed out than the scene's.
7. **Sharpness, grain and noise differ.** A crisp, noise-free subject over a grainy phone-video background.
8. **Motion blur and camera shake differ.** The camera shakes but the subject stays perfectly steady, or the subject has no blur when it moves fast.
9. **Edges.** Halos, shimmering outlines, hair that looks cut out.
10. **Scale and perspective.** The subject's eye line and horizon don't agree with the camera height.
11. **Temporal drift.** Faces flicker, hands stretch, products change shape or logos wobble between frames.

---

## 3. The lighting-match method

Do this **before** you write a prompt. It is the most important step in this guide.

### Step 1: Read the light in your plate (the scene that stays)

Look at the background video or environment reference and write down:

| Question | Example answer |
|---|---|
| Where is the **key light** (main light)? | Low sun, camera-left, behind the subject (backlight) |
| **Hard or soft**? (Sharp shadow edges = hard) | Hard |
| **Color temperature**? | Warm golden, around 3200K |
| **Fill** (how dark are the shadows)? | Shadows are fairly open, lifted by a blue sky |
| **Practicals** (lamps, screens, signs in frame)? | None |
| **Bounce colors** (big colored surfaces nearby)? | Tan concrete below, so warm bounce from below |
| **Time and weather** | About 20 minutes before sunset, clear, light haze |
| **Camera** | Handheld, 35mm look, slight grain, shallow depth of field |

### Step 2: Make your references agree with it

This matters most. When your character reference has warm side light and your environment reference has flat fluorescent light, **Seedance tries to split the difference** and the lighting looks wrong on both.

- Pick character and product references that are lit **as close as possible** to the plate (same direction, same warmth).
- If you can't find one, use **neutral, even, soft-lit** references (front-facing, overcast or studio softbox). Neutral light is much easier for the model to relight than strong light going the wrong way.
- For Genjutsu, use **front-facing, full-body** references with clear face and costume detail.
- Don't use references with baked-in effects: heavy filters, beauty-mode skin, strong color grades or lens flares.

### Step 3: Put the light into words in the prompt

Describe the lighting of the scene the subject must fit into, then say that the subject shares it. Always cover **direction, quality, color, and the interaction** (shadow, bounce, reflection).

> Lit by the same low golden sun as the background, coming from behind camera-left, giving a warm rim light on her hair and shoulder. Her face is in soft open shade filled by blue skylight. She casts a long hard shadow toward camera-right that matches the other shadows in the scene. Warm bounce from the concrete below.

### Step 4: Check it (see the QC checklist in Section 7)

---

## 4. Seedance: how to prompt

Seedance follows plain natural language. Write each prompt like a **shot brief for a camera crew**, not a list of keywords.

### Prompt order

1. **Subject**: who or what is in frame (anchor it to a reference)
2. **Action**: what they do, step by step, in time order
3. **Scene**: where
4. **Camera**: shot size, lens feel, movement
5. **Lighting**: direction, quality, color, interaction (Section 3)
6. **Look and texture**: film stock, grain, lens character
7. **Sound or dialogue**: spoken lines go in "double quotes" and Seedance generates the voice and lip sync
8. **Consistency lock**: what must not change

**Spend your words on motion, not appearance.** The reference image already shows what the person looks like. "Camera slowly orbits her as she turns to look over her shoulder" does more than three more lines describing her face.

### Using references (@ tags)

Every uploaded file gets a handle: `@Image1`, `@Image2`, `@Video1`, `@Audio1`, and so on.

- `@Image` = **identity and appearance** (people, products, places, style)
- `@Video` = **motion and camera movement**
- `@Audio` = **rhythm, pacing, voice**

**Always say what each reference is for.** The model will not work out the connections on its own. Start with **3–5 references, each with a single job**. More references dilute each one.

Add lock phrases like:
- "maintain exact appearance from @Image1"
- "consistent character throughout, no deformation or drift"
- "product label and logo stay sharp and unchanged"

### Template

```
@Image1 is the main character. @Image2 is the location. @Video1 is the camera movement reference only.

[SUBJECT] The woman from @Image1, in a faded olive jacket,
[ACTION] walks toward camera, slows down, then glances over her left shoulder and smiles slightly.
[SCENE] A quiet street in @Image2 at golden hour, a few parked cars, light traffic in the distance.
[CAMERA] Medium shot, 35mm, handheld, slow push-in that follows the movement in @Video1.
[LIGHT] Low warm sun behind her, camera-left, giving a golden rim on her hair and shoulders. Her face is in soft open shade with cool fill from the sky. Her long shadow falls toward camera-right, matching the parked cars' shadows. Warm bounce from the pavement.
[LOOK] Natural color, slight film grain, shallow depth of field, gentle lens halation on highlights.
[SOUND] Distant traffic, footsteps on pavement.
[LOCK] Maintain exact face and jacket from @Image1. Consistent character, no drift. No text on screen.
```

### Example prompts

**Product in a real-looking scene (ad)**
```
@Image1 is the product (a matte black water bottle). Keep its shape, label and logo exactly as in @Image1.
A hand picks the bottle off a wooden cafe table next to a window and lifts it out of frame.
Close-up, 50mm, locked-off camera, shallow depth of field.
Soft overcast daylight from the window on camera-right. Cool neutral light with a soft highlight along the right edge of the bottle, and a faint reflection of the window in its matte surface. A soft contact shadow under the bottle that disappears as it lifts. Warm wood bounce on the bottom of the bottle.
Natural color, light grain. Quiet cafe ambience.
```

**Talking to camera with dialogue**
```
@Image1 is the presenter. Maintain her exact appearance.
She sits in a small home studio and speaks directly to camera: "Most AI videos look fake because the light is wrong. Here's how to fix it."
Medium close-up, 50mm, locked-off tripod.
Key light: a large soft window on camera-left, slightly warm. Gentle falloff to shadow on the right side of her face. A small practical desk lamp behind her, out of focus, adds warm spill on the wall. Catchlights from the window visible in her eyes.
Natural skin texture with visible pores, no beauty smoothing. Light grain.
```

**Night neon (hardest lighting to fake)**
```
@Image1 is the man. @Image2 is the alley.
He steps out of a doorway into the rain-soaked alley from @Image2, pulls up his hood and looks down the street.
Wide shot, then slow push to medium. 35mm handheld.
Mixed lighting: magenta neon sign camera-right casts pink light on the right side of his face and jacket. Cool blue streetlight from behind gives a rim on his shoulders. Wet ground reflects both colors under his feet. Raindrops catch the neon. Deep shadows, but not crushed.
Visible rain, slight motion blur on fast movement, film grain.
Consistent character, no drift.
```

---

## 5. Genjutsu: how to use it

### Step-by-step

1. **Film or pick a good source clip** (see "source rules" below). It should be 3–30 s long.
2. **Pick the mode**:
   - Changing **one thing** (outfit, product, one person, the background)? Use **Object Swap**.
   - Keeping only the **movement and camera** and rebuilding the rest? Use **Motion Transfer**.
3. **Upload reference images** (up to 40), sorted by role: character, wardrobe, product, location.
4. **Write the brief in two parts**: what **stays**, then what **changes** (template below).
5. **Test at 480p first** (about 40 credits for 15 s). Check it with the QC checklist.
6. **Fix and re-run**, changing one thing at a time.
7. **Final render at 1080p** (about 144 credits for 15 s).

### Source clip rules (good input gives good output)

- **Stable framing and clear motion.** Avoid heavy shake, whip pans and people passing in front of the subject.
- **Keep the subject fully visible.** Hands and feet leaving and re-entering the frame are where artifacts happen.
- **Even, readable light on the subject.** Blown-out highlights and crushed shadows give the model nothing to work with.
- **Shoot the light you want in the final.** For a sunset result, film at sunset. Genjutsu keeps your source's light and camera, so the source's lighting is your lighting.
- **Shorter takes stay steadier.** Drift, finger stretch and face flicker build up in long takes. Shoot several 5–10 s pieces instead of one 30 s take when you can.

### Brief template: "Protect, then change"

Treat the source clip as the authority. **Describe what must be protected before you describe the change.**

```
PROTECT (keep exactly from the source video):
- All body motion, timing and choreography
- Camera path, shot size and framing
- Original lighting direction and color: warm window light from camera-left, soft shadows to the right
- Background, props and everything not listed below

CHANGE:
- Replace the person with the character in the references (face, hair, build)
- Outfit: the grey hoodie from the wardrobe reference

MATCH:
- New character is lit by the same window light from camera-left, same warmth, same shadow softness
- Keep the contact shadows under feet and hands as in the source
- Keep the source's grain, sharpness and motion blur
```

### Common problems

| Problem | Likely cause | Fix |
|---|---|---|
| Face flickers or changes | Weak or low-res face reference, or angles that don't match | Add clear front and 3/4 face references, shorten the clip |
| Hands stretch or have wrong fingers | Fast hand motion, hands leave the frame | Shoot slower hand movement, keep hands in frame, shorten the take |
| Feet float or slide | No visible ground contact in the source | Keep feet in frame, say "keep contact shadows and ground contact" |
| Swapped product wobbles or changes shape | Product reference from one angle only | Add references from the angles the product is seen from in the clip |
| Subject looks pasted on | Reference lighting fights the plate | Redo Section 3; use neutral soft-lit references |
| Framing changed | Brief didn't lock the shot | Add "same shot size and framing as the source" under PROTECT |

---

## 6. Workflow for a full piece

1. **Plan**: write the shot list. For each shot, choose Seedance (new) or Genjutsu (from footage).
2. **Lighting bible**: for each location, write one lighting description (Section 3, Step 1) and **reuse it word for word** in every shot there. Matching words give matching light from shot to shot.
3. **Reference kit**: one folder per character, product and location, with neutral-lit, high-res, clean images from several angles.
4. **Test cheap**: 480p for everything first.
5. **QC** every clip (Section 7). Fix, then re-run.
6. **Final renders** at full resolution.
7. **Finish in an editor** (CapCut, Premiere, DaVinci Resolve). This is where "AI clips" become "a video":
   - **One color grade over everything** so all shots share the same black level, contrast and palette.
   - **Add the same film grain to every shot.** Uniform grain hides small mismatches and ties AI and real footage together.
   - **Match sharpness.** Soften a too-crisp AI shot slightly to match real footage.
   - **Sound design**: room tone, footsteps, ambience. Real sound makes the eye accept the image.
   - **Cut on motion**, and don't hold a shot longer than it needs to be. Most artifacts show up late in a take.

---

## 7. Realism QC checklist

Watch each clip **at full screen, at least once in slow motion or frame by frame**, on the biggest and sharpest screen you have.

**Light**
- [ ] Light hits the subject from the same direction as the rest of the scene
- [ ] Subject and scene share the same warmth or coolness
- [ ] Shadow softness matches (hard sun = hard shadows everywhere)
- [ ] Nearby colored surfaces or lights tint the subject (bounce and spill)
- [ ] Reflections in eyes, glasses, glossy products and wet floors show the right environment

**Contact and space**
- [ ] Feet and objects have contact shadows and don't float or slide
- [ ] The subject's size and perspective fit the camera height and horizon
- [ ] Depth of field is consistent (a subject at the same distance as blurry background items is equally blurry)

**Texture**
- [ ] Grain and noise match across subject and background
- [ ] Sharpness matches; no too-crisp subject on a soft plate
- [ ] Motion blur matches movement speed; camera shake affects everything together
- [ ] Skin has natural texture (not plastic or waxy)

**Stability over time**
- [ ] Face stays the same person from first frame to last
- [ ] Hands have the right fingers the whole time
- [ ] Logos, text and product shapes don't warp
- [ ] Edges and hair don't shimmer or halo
- [ ] No flicker in brightness or color

If a clip fails **one light item**, fix the references or lighting description and regenerate. That rarely gets fixed in the edit. If it fails **one texture item**, you can usually fix it in the edit with grain, blur or grading.

---

## 8. Use it responsibly

Genjutsu can put a different person into real footage, and Seedance can make realistic people say things. Keep it clean:

- **Only use someone's face or voice with their permission.** Don't recast real people (celebrities, exes, coworkers) without consent.
- **Label AI content** where platforms ask for it (TikTok, YouTube and Instagram all have AI-content disclosure settings). Undisclosed realistic AI of real people can get content removed or accounts struck.
- Don't make fake news, fake testimonials or fake endorsements.
- Check the platform's terms before using generated content commercially.

---

## Sources

- [Higgsfield Genjutsu](https://higgsfield.ai/genjutsu) and [Meet Higgsfield Genjutsu (blog)](https://higgsfield.ai/blog/higgsfield-genjutsu)
- [Riffkit: How to Use Higgsfield Genjutsu](https://riffkit.ai/blog/how-to-use-higgsfield-genjutsu)
- [Rekreate: Genjutsu limits and pricing](https://rekreate.ai/news/higgsfield-genjutsu)
- [Dreamina: Genjutsu-style workflow](https://dreamina.capcut.com/ai-video/higgsfield-ai-genjutsu)
- [Cachephoto: Genjutsu video-to-video](https://www.cachephoto.com/en/cineblog/higgsfield-genjutsu-video-a-video/)
- [Higgsfield: Seedance 2.0 Prompting Guide](https://higgsfield.ai/blog/seedance-prompting-guide)
- [fal: Seedance 2.0 Prompting Guide](https://fal.ai/learn/tools/seedance-2-0-prompting-guide)
- [fal: Seedance 2.5 vs 2.0](https://fal.ai/learn/devs/seedance-2-5-vs-seedance-2-0)
- [BytePlus ModelArk: Seedance 2.0 prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2222480)
- [Magic Hour: Seedance 2.0 reference guide](https://magichour.ai/blog/seedance-20-reference-guide)
- [Clipdance: Reference images in Seedance 2.0](https://clipdance.ai/blog/ai-video-reference-images-guide)
- [Atlas Cloud: Seedance 2.0 all-round reference](https://www.atlascloud.ai/blog/case-studies/generative-ai-model-seedance-2-0-a-guide-to-all-round-reference)
