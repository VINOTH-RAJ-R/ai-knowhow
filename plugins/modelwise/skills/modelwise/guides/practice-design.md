# How a creative director turns a request into a design

A prompt writer goes from words straight to a picture. A creative director goes request → brief → insight → three really different ideas → judge → produce. In production, the image model makes the picture, and people set the type, logo and legal copy. Use this guide for every poster, banner, social post, launch graphic and ad visual. `guides/art-direction.md` covers the craft of each image. This guide covers the thinking that comes before it.

Sources: Dave Trott on the single thought behind a brief (davetrott.co.uk), Jenni Romaniuk and Ehrenberg-Bass on distinctive brand assets (marketingscience.info, marketingweek.com), Monzo's brand designer Q&A on coral and the card-edge device (community.monzo.com), Robinhood's visual identity (robinhood.com/us/en/newsroom/a-new-visual-identity), CRED's NeoPop system, LinkedIn's single-image ad specs (linkedin.com/help/lms/answer/a426534), WCAG 2.2 contrast (w3.org), OpenAI's image-generation guide on text and layout limits (developers.openai.com).

## 1. Write the brief before any picture

| Field | What a senior team writes |
|---|---|
| Objective | The one behaviour wanted: notice and remember the name, click to learn more, register, share. |
| Audience and insight | Who sees it and one human tension in their own words. "Small-business owners dread the end-of-month invoice chase" is an insight. "The app automates invoicing" is a product fact. |
| Proposition | One sentence, one thought, no "and". If the user's copy is the whole message (a short announcement), the proposition is that announcement sharpened to one thought. |
| Reason to believe | One provable fact that is allowed to be shown. Leave it out rather than invent one. |
| Mandatories | Logo, legal and regulatory lines, dates, URL, language. These are placed by a person in the design tool, not generated. |
| Tone | Three adjectives and one thing it is not ("confident, clear, warm; not salesy"). |
| Channel and format | Where it runs, with platform size and safe zones (section 4). |
| Category look | What competitors' posts look like, so this one can stand apart. |

**Research the brand itself,** not only the topic: what the company does, who it serves (consumers, distributors, businesses), its website and recent social posts, and any recurring device (a shape, a frame, a colour treatment, an illustration style). Winners own one colour plus one device and reuse it: Monzo's hot coral and card edge, Robinhood's neon accent on black, CRED's NeoPop system. If you can't find a device, propose one drawn from the logo or brand colours and label it an assumption.

## 2. Name the category clichés, then design away from them

List 3–5 clichés for the category before writing any route. In finance they are rising bars and arrows, upward chart lines, coins and cash, rockets, piggy banks, handshakes, lighthouses and compasses, and generic glowing cards floating on a gradient. A cliché is acceptable only when it is transformed into something the brand owns. A literal bar chart is never acceptable.

Put the cliché list in the answer so the user sees the thinking. Inside the image prompt, steer with the positive description of the hero, and keep the Avoid line generic ("no stock finance imagery"). Naming a motif can pull it into the image.

## 3. Three territories, really different

A territory is a different idea about why the audience should care. A different colour, style or layout of the same idea doesn't count. Make every pair of routes differ on at least two of these four axes:

| Axis | Choices |
|---|---|
| Focal element | type-led (the words are the hero) · object/product-led (a product or UI object) · human-led (a real-life moment: hands, a desk, a phone, an over-the-shoulder view) · graphic-led (the brand device or a pattern system) |
| Visual metaphor | what the picture stands for: a reveal, an arrival, an invitation, a signal, a key, a new entry in a familiar place |
| Tonal register | calm and editorial · bold and urgent · warm and human · precise and technical |
| Medium | from the style families in `guides/art-direction.md`: 3D, glass and light, photography, typographic, paper-cut, abstract geometry, UI-led |

**Default spread for three routes:** one type-led, one object- or product-led, one human- or graphic-led. Each route uses a different medium **and a different taste direction** from the industry's list in `guides/creative-taste.md`, with one signature craft decision.

**Swap test.** If changing the background, palette or medium would turn one route into another, they are the same idea. Replace one.

For each route, write:
- a name and a one-line idea,
- its four axes,
- the hero in one sentence, plus what it deliberately leaves out,
- how the user's exact copy is staged (scale, position, relation to the hero),
- the prompt,
- one risk (what could go wrong in rendering or reception).

## 4. Judge before recommending

Score each route on these checks, in order, and recommend the one that passes the most. Say why in one line.
1. **Thumbnail test:** the focal point and the message survive at about 1 cm wide.
2. **One-second test:** a stranger could say the message after a glance.
3. **Distinctive:** would it be recognised with the logo covered? Could a competitor run it unchanged? If yes, it fails.
4. **Brand fit:** palette, type, tone and industry (`guides/industry-lens.md`).
5. **Provable and compliant:** no claim the brand can't support; regulated elements have room.
6. **Channel fit:** crop, safe zones, contrast on a phone.

## 5. Produce it the way a studio would

Image models can't reliably place text, keep brand elements consistent or follow a precise layout (OpenAI's own guide says so). Studios therefore split the work:
- **Preview prompt** (each route): the full image with the user's exact copy, for judging the idea in ChatGPT or similar.
- **Production plate** (the recommended route only): the same scene with no text, no logo and no UI chrome. Reserved zones are described as rectangles in percent of the canvas, "kept clear and calm, still filled with the background". Check a zone by laying a bright box over it in the design tool; if anything pokes through, regenerate.
- **Layout spec** for the designer: grid and margins; each text level with font, size (as % of canvas height) and weight; anchor positions; logo version and position; legal block position; the text colour and its contrast ratio (`scripts/palette.py`).
- **Mandatories checklist:** every required element, to be set as real type in Figma or Canva.

Iterate one variable at a time and keep a log of the prompt and settings for each approved plate. Seeds don't carry across model versions.

## 6. Channel sizes (check the platform's help page before shipping)
- **LinkedIn single image:** 1.91:1 at 1200×628, 1:1 at 1200×1200, 4:5 at 720×900 (vertical shows on mobile only). A 2:1 design crops slightly to 1.91:1, so keep 5% clear at the sides.
- **Instagram feed:** 4:5 at 1080×1350. Stories and Reels: 9:16 at 1080×1920. Keep the top ~14%, bottom ~35% and sides ~6% free of text (bottom ~40% if there's a disclaimer).
- **Website hero:** the sides crop on narrow screens, so keep faces, products and text away from the edges and plan a separate mobile crop.
- **Image API sizes:** edges in multiples of 16. Examples: 2:1 → 1536×768; 1.91:1 → 1536×800; 4:5 → 1024×1280.
- **Contrast** (WCAG 2.2): 4.5:1 for normal text, 3:1 for large text (18pt and up, or 14pt bold). Text inside images has to meet the same ratios.

## 7. Regulated categories (finance, health, alcohol, crypto, gambling)
- **Find the mandatory elements** for this category and market. If the category and market match a section of `guides/regulated.md`, use it; otherwise research them, or ask the user for their compliance team's list.
- **Set them as real type** from approved text. Nothing regulatory is generated by the image model.
- **The visual makes no promise.** No imagery that implies a return, a cure or a guaranteed outcome.
- **Keep the user's copy exactly as written.** Don't add mandatory elements to their headline. Reserve space for them in the plate, list them in the mandatories checklist, and ask for the values you don't have under "To improve the result".
- **Flag the compliance sign-off,** and any filing with the regulator.
