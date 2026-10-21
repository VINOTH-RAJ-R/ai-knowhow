# The expert lens: think like the top practitioner in that industry

Every prompt is written for a real industry, audience and brand. A beautiful result in the wrong genre is still wrong. A fantasy portal for a fund house fails, and so does a playful, emoji-filled email from a hospital. Before you write any prompt (image, code, copy, data, research), apply the lens below.

## The procedure (every task, every type)

1. **Industry and audience.** Name the industry, who will see or use the output, and what they must feel or do. ("Indian retail investors scrolling LinkedIn. They should feel confident and informed, and click to learn more.")
2. **The top practitioner.** Name the person who would own this task at the best company in that industry. Examples: "head of brand design at a leading fintech", "staff backend engineer at a payments company", "senior copywriter at a hospital network", "lead data analyst at a D2C brand". Write the prompt as that person would.
3. **Their conventions and their refusals.** What would they always do, and what would they refuse? Use the playbook below.
4. **Brand personality.** 3–5 adjectives from the industry plus the user's brand cues. Put them in the prompt.
5. **Brand-fit check before you send.** Answer all four. If any answer is "no", change the concept, not just the words.
   - Would the brand's own team approve and publish this?
   - Does it read as *this industry* within one second?
   - Is it free of genre drift (fantasy, mythic, religious or afterlife, horror, sci-fi, gaming) unless the brand is in that genre?
   - Is it free of compliance and claim risk for this industry?

If the industry isn't in the playbook, reason it out with the same five steps and say so in one line.

## Playbook

### Fintech and financial services (banking, payments, mutual funds, insurance, wealth)
- **Personality:** trustworthy, clear, calm confidence, modern, optimistic, human.
- **What the best brands do:** bright, airy, contemporary compositions. Product- and UI-led visuals: app screens, cards and dashboards shown as clean objects with soft, realistic depth. Brand-shape geometric systems. Real-life moments photographed naturally (planning at a desk, a family at home, a professional on a phone). Daylight or soft studio light. Generous whitespace and a strong type hierarchy. Data drawn as elegant, simplified charts with no real numbers.
- **Refuse:** fantasy, epic or mystical scenes (portals, glowing doorways, temples, ancient stone, mountains in mist, god-rays, smoke). Dark or ominous moods. Money clichés (raining cash, piles of gold coins, rockets to the moon, casino energy). Aggressive red. Stock-chart screenshots. Anything implying guaranteed returns.
- **Copy:** plain, precise, no hype ("guaranteed", "best returns", "risk-free"). Short sentences.
- **Engineering:** money as integer minor units or decimal, never float. Idempotent payment operations. Audit logs. Authentication and authorisation on every endpoint. Encryption of personal data at rest and in transit. Card data under PCI DSS. Accessibility (WCAG AA).
- **Compliance:** the regulator's mandatory disclaimers go in as real text, never generated. No celebrities in mutual fund ads (India, SEBI). The issuing entity is named correctly.

### Healthcare, pharma and wellness
- **Personality:** caring, competent, calm, reassuring, evidence-based.
- **Best practice:** soft natural light, real clinical or home settings, diverse real people, clean information design, plenty of white space.
- **Refuse:** fear imagery, gore, miracle claims, before/after without substantiation, dramatic or dark lighting.
- **Copy:** plain language at a reading age of about 12, no diagnosis or promised outcomes.
- **Engineering:** patient-data privacy (HIPAA or local equivalents), consent, audit trails, accessibility.

### Education and edtech
- **Personality:** encouraging, clear, curious, inclusive.
- **Best practice:** bright and friendly scenes, learners in action, simple illustration systems, clear progress metaphors (paths, steps, badges).
- **Refuse:** exam-fear imagery, elitist cues, cluttered infographics.
- **Engineering:** child-data protection where minors are involved, accessibility, offline and low-bandwidth tolerance.

### B2B SaaS and enterprise tech
- **Personality:** capable, precise, efficient, confident.
- **Best practice:** product UI as the hero, clean isometric or 2.5D diagrams, crisp brand gradients, customer-outcome framing.
- **Refuse:** generic "global network of glowing dots", stock handshakes, cyberpunk neon (unless security branding calls for it).
- **Engineering:** multi-tenancy, permissions, observability, API versioning, SOC 2-style controls.

### Consumer apps and consumer tech
- **Personality:** friendly, simple, delightful, fast.
- **Best practice:** device mockups in real hands and real places, bold colour blocks, playful but tidy motion and illustration.
- **Refuse:** clutter, dark patterns in UI copy.

### E-commerce, retail and D2C
- **Personality:** desirable, honest, energetic.
- **Best practice:** product as hero with true-to-life colour and texture, lifestyle context, clean price and offer hierarchy.
- **Refuse:** fake scarcity, misleading imagery of the product, illegible offer text.
- **Engineering:** performance (Core Web Vitals), SEO, inventory consistency, payment reliability.

### Food, restaurants and hospitality
- **Personality:** warm, appetising, inviting.
- **Best practice:** natural light food photography, texture and steam, human hands, real tables.
- **Refuse:** cold or blue-tinted food, plastic-looking renders, dark moody scenes for family brands.

### Real estate
- **Personality:** aspirational, trustworthy, grounded.
- **Best practice:** golden-hour architecture, real interiors, clean floor-plan graphics.
- **Refuse:** impossible renders presented as real, misleading scale.

### Festivals, culture and religion
- **Personality:** respectful, warm, authentic.
- **Best practice:** motifs verified by research, traditional palettes adapted to the brand, illustration or paper-cut styles.
- **Refuse:** depicting deities unless asked, mixing traditions, stereotypes, commercial cues that trivialise the occasion.

### Luxury and fashion
- **Personality:** refined, confident, rare.
- **Best practice:** restraint, negative space, editorial photography, texture and craft, a small serif or refined sans.
- **Refuse:** clutter, discount energy, loud gradients.

### Kids and family
- **Personality:** joyful, safe, warm.
- **Best practice:** rounded shapes, bright friendly palettes, illustration, parents and children together.
- **Refuse:** anything frightening, unsafe situations, realistic children's faces where privacy matters.

### Government, NGO and public sector
- **Personality:** credible, inclusive, clear, accountable.
- **Best practice:** real communities, accessible information design, plain-language copy.
- **Refuse:** partisan cues, poverty imagery that removes dignity.

### Entertainment and gaming
- **Personality:** bold, immersive, dramatic.
- **Best practice:** this is where cinematic light, epic scale, fantasy worlds and atmospheric haze belong.
- **Refuse:** generic stock aesthetics; style mismatched to the game's genre.

## Genre drift: the most common failure

Words like "cinematic", "epic", "monumental", "volumetric rays", "haze", "mist", "ethereal", "mystical", "portal", "doorway of light", "ancient stone" and "dust in the light" pull image models toward fantasy and spiritual scenes. Use them only for entertainment, gaming or festival work where that mood fits. For corporate, fintech, health and SaaS, use "contemporary, grounded, real-world, daylight, clean studio lighting, crisp, product-led, editorial".
