# Sabrina

AI character used for video remakes (Genjutsu / Seedance 2.5 on Higgsfield).

## Look
- Long, voluminous jet-black curly hair with a side part and laid edges
- Warm brown skin, full glossy lips, long lashes, small stud earrings
- Curvy hourglass figure
- Signature outfit: heather-grey cropped tee, colourful comic-print high-waisted shorts, white low-top sneakers, gold bracelet, pink nails

## References
- `sheet1.png`, `sheet2.png` — full consistency sheets (best for Seedance 2.5 omni-reference)
- `fullbody_front.png` — single front full-body pose (best for Genjutsu)
- `face_front.png` — front face close-up (identity anchor)

## Higgsfield
- Element ID: `7fb5b922-08df-48ad-8402-8feb9566f4ce` (name: Sabrina, category: character)
- Media IDs:
  - sheet1: `122cecf6-49fd-49ea-ac15-c11c03351c16`
  - sheet2: `c68b3ca2-16f8-4d9d-b33f-b83f0326842b`
  - fullbody_front: `c18b0dc9-e711-4591-8579-558a4227ef79` (use for Genjutsu)
  - face_front: `f64d98bd-f850-4a70-a6e0-dd2f3aa86662`

## Variants
- Cropped hoodie + leggings full body (image job): `d278cb60-08af-41a1-99c0-565e2331bcff`
- Hoodie/joggers full body (image job): `04b94967-3697-42de-9738-77e381ed916c` — use for Genjutsu on hip-focused / twerk-style dances; the crop-top + shorts reference gets NSFW-flagged on those.

## Remake log
| Date | Source video | Model | Ref | Res | Result |
|---|---|---|---|---|---|
| 2026-10-02 | `945d38d7-8a27-42dd-87d5-a130b12dab99` (bedroom hip-shake dance, 6s) | Genjutsu | fullbody_front | 480p | NSFW-flagged (x2) |
| 2026-10-02 | same | Genjutsu | hoodie variant | 480p | ✅ `0a752619-908c-44d8-9575-bd3efad0f44f` |
| 2026-10-02 | same | Genjutsu | leggings variant | 480p | NSFW-flagged |
| 2026-10-02 | `98bb5482-95be-45bc-a12d-bfefe429b16a` (locker room look-back + gym mirror selfie, 10s, 3 cuts) | Genjutsu | leggings variant | 480p | ✅ `d30af5eb-6700-4ee6-bbd7-e8bae28d604c` |
| 2026-10-02 | `4fba8f08-969a-4c11-aa67-379796b4718f` (kitchen leggings try-on, turns/bends, 22s) | Genjutsu | leggings variant | 480p | ✅ `8d681fa6-2d9c-4f11-966a-3191550d895b` |
