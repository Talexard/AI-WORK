# Custom Craft Carpentry & Remodeling: Demo Notes

**Site files:** `demos/custom-craft/` (static HTML, CSS and JS: no build step, free to host)
**Previews:** `demos/previews/custom-craft-desktop.png` (first screen), `custom-craft-desktop-full.png`, `custom-craft-mobile.png`

**Design (v2, Nov 4 2026):** based on `research/creative-web-design-study.md`. Big editorial serif headline mixing upright and italic letters. Warm cream background with one safety-orange accent. Craft-themed details: a sliding tape-measure strip, a blueprint section where a house drawing draws itself as you scroll, a taped-on photo frame and a spinning badge. Also a scrolling services ticker and a numbered services list. Respects the phone's reduce-motion setting, and all content still shows if JavaScript is off. No code libraries.

## What's real vs. what needs confirming
**Real (from the Champaign County Chamber listing):** business name, 219 E Court St, Urbana, OH 43078, (937) 561-2262, solo operator, residential remodeling and construction, chamber member.

**Assumed (confirm with the owner before launch):**
- The exact list of services (kitchens, baths, trim, decks, additions, repairs)
- The towns served
- The FAQ answers, and that estimates are free and written
- Whether they want to be reached by text as well as by phone

**Placeholders, clearly marked in the demo:**
- 7 photo spots (1 featured photo plus 6 gallery photos): replace with the owner's own job photos.
- 3 review cards: replace with real Google reviews, quoted word for word. **Never write reviews ourselves.**
- The estimate form shows a "demo only" message. At launch, connect it to Netlify Forms or Formspree.

## Before launch, remove
- The `<meta name="robots" content="noindex, nofollow">` line in `index.html`
- The dark "Demo concept" banner at the top

## How to put up a free preview link (5 minutes)
1. Go to https://app.netlify.com/drop (a free Netlify account is required).
2. Drag the `demos/custom-craft` folder onto the page.
3. You get a link like `something.netlify.app`. Rename it in Site settings to `customcraft-preview`.
4. Text that link to the owner.

## The pitch hook
- Their current site shows a Squarespace **"Website Expired"** page.
- Their domain `customcraftremodel.com` (registered through Squarespace Domains) **expires Dec 26, 2026.**
