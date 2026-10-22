# The expert lens: think like the top practitioner in that industry

Every prompt is written for a real industry, audience and brand. A beautiful result in the wrong genre is still wrong. A fantasy portal for a fund house fails, and so does a playful, emoji-filled email from a hospital. Before you write any prompt (image, code, copy, data, research), apply the lens below.

## The procedure (every task, every type)

1. **Industry and audience.** Name the industry, who will see or use the output, and what they must feel or do. ("Clinic managers reading email between patients. They should feel the tool saves them time, and book a demo.")
2. **The top practitioner.** Name the person who would own this task at the best company in that industry. Examples: "head of brand design at a leading fintech", "staff backend engineer at a payments company", "senior copywriter at a hospital network", "lead data analyst at a D2C brand". Write the prompt as that person would.
3. **Their conventions and their refusals.** What would they always do, and what would they refuse? Use the playbook below.
4. **Brand personality.** 3–5 adjectives from the industry plus the user's brand cues. Put them in the prompt.
5. **Brand-fit check before you send.** Answer all four. If any answer is "no", change the concept, not just the words.
   - Would the brand's own team approve and publish this?
   - Does it read as *this industry* within one second?
   - Is it free of genre drift (fantasy, mythic, religious or afterlife, horror, sci-fi, gaming) unless the brand is in that genre?
   - Is it free of compliance and claim risk for this industry?

If the industry isn't in the playbook, reason it out with the same five steps and say so in one line.

**How the top practitioner actually works** (read the one that matches the task):
- Coding, frontend, debugging, agents → `guides/practice-engineering.md`: the senior engineer's brief, plus overlays for fintech, banking, investments, IT services and startups.
- Posters, banners, social and ad visuals → `guides/practice-design.md`: the creative director's brief, category clichés, three distinct territories, judging, and plate plus layout-spec production.
- Video, copy, research, data → `guides/practice-content.md`: the producer's, copywriter's and analyst's checklists, plus content rules by industry.

## Playbook

### Fintech and financial services (banking, payments, mutual funds, insurance, wealth)
- **Personality:** trustworthy, clear, calm confidence, modern, optimistic, human.
- **What the best brands do:** own one colour and one device and reuse it everywhere (Monzo's hot coral and card edge; Robinhood's neon accent on black; CRED's NeoPop system). Show the product or a feature, often exaggerated, instead of abstract money. Bright, airy, contemporary compositions. Product- and UI-led visuals: app screens, cards and dashboards shown as clean objects with soft, realistic depth. Brand-shape geometric systems. Real-life moments photographed naturally (planning at a desk, a family at home, a professional on a phone). Daylight or soft studio light. Generous whitespace and a strong type hierarchy. Data drawn as elegant, simplified charts with no real numbers.
- **Refuse:** fantasy, epic or mystical scenes (portals, glowing doorways, temples, ancient stone, mountains in mist, god-rays, smoke). Dark or ominous moods. Money clichés (rising bars and arrows, raining cash, piles of gold coins, rockets to the moon, piggy banks, handshakes, casino energy). Aggressive red. Stock-chart screenshots. Anything implying guaranteed returns.
- **Copy:** plain, precise, no hype ("guaranteed", "best returns", "risk-free"). Short sentences. Explain jargon. No jokes about money worries.
- **Engineering:** money as integer minor units with a currency code, never float. Idempotency keys on money-moving calls. Append-only double-entry ledger. Reconciliation. Signed, deduplicated webhooks. Audit logs. Maker-checker for manual money actions. Card data kept out of scope with tokenisation (PCI DSS). Details in `guides/practice-engineering.md`.
- **Compliance:** the regulator's mandatory disclaimers go in as real text, never generated. No testimonials, rankings or return projections where the regulator bans them. The issuing entity is named correctly. For a market covered by `guides/regulated.md`, use its section.

### Banking
- **Personality:** reassuring, precise, established, unflashy, human.
- **Best practice:** real customers and real moments, product clarity (fees and rates shown together), strong service tone, consistent brand device across branch, app and social.
- **Refuse:** guarantee language outside guaranteed products, fear-led security messaging, cluttered rate tables, invented legal lines.
- **Engineering:** data stored and processed in the region the regulator requires. Core-banking adapters with cut-off and batch awareness. Ticketed change with UAT sign-off and rollback. Segregation of duties. Immutable audit logs. Personal and KYC data masked outside production.

### IT services and enterprise IT
- **Personality:** dependable, expert, structured, partner-like.
- **Best practice:** client outcomes with named, permitted proof; clear architecture diagrams; people at work rather than abstract tech.
- **Refuse:** globes of glowing dots, circuit-board backgrounds, padlocks, unprovable "best" and "leading" claims, fabricated logos or certifications.
- **Engineering:** client standards first, boring supportable technology, documentation and runbooks as deliverables, SLAs, environments and release notes, handover-ready code.

### Startups
- **Personality:** sharp, candid, founder-credible, a clear point of view.
- **Best practice:** a strong single idea over polish, real early proof (users, pilots, waitlist), the founder's voice, one distinctive device used consistently from day one.
- **Refuse:** inflated traction, borrowed big-brand gloss with no idea behind it, jargon.
- **Engineering:** smallest slice that tests the riskiest assumption, YAGNI, deliberate recorded tech debt, managed services. Never skimp on tests for money, auth and data-loss paths. Regulated startups use their sector's overlay.

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

### Manufacturing and industrial
- **Personality:** reliable, precise, engineered, safety-first.
- **Best practice:** real plants, products and people at work; technical clarity (specs, tolerances, certifications); case studies with measured outcomes.
- **Refuse:** unsafe practices in imagery (missing protective equipment), vague "world-class quality" claims, invented certifications.
- **Engineering and operations:** safety and quality systems (ISO 9001, ISO 45001 where relevant), traceability, OT/IT separation, downtime cost in every decision.

### Logistics, supply chain and mobility
- **Personality:** dependable, fast, transparent, efficient.
- **Best practice:** real-time visibility and tracking UI, clear service levels, maps and flows drawn simply, the people who move goods.
- **Refuse:** delivery promises the network can't keep, cluttered route maps.
- **Engineering and operations:** event-driven tracking, idempotent status updates, exception handling (delays, damages, returns), SLA measurement.

### Energy, utilities and telecom
- **Personality:** dependable, responsible, clear, future-focused.
- **Best practice:** plain-language bills and tariffs, outage communication that leads with impact and restore time, real infrastructure and communities.
- **Refuse:** greenwashing (unsubstantiated "green" or "net zero" claims), fear-led safety messaging, jargon in customer communication.
- **Engineering and operations:** critical-infrastructure security, regulatory reporting, high-availability design, field-workforce safety.

### Professional services (consulting, legal, accounting, agencies)
- **Personality:** expert, rigorous, discreet, partner-like.
- **Best practice:** a point of view backed by evidence, answer-first structure, named credentials, client confidentiality.
- **Refuse:** client names or results without permission, overclaiming, generic thought leadership.
- **Compliance:** professional-body rules on advertising and confidentiality, conflict checks.

### Media and publishing
- **Personality:** credible, timely, distinctive voice.
- **Best practice:** a strong headline with accurate framing, sourcing standards, clear separation of editorial and sponsored content.
- **Refuse:** misleading headlines, unlabelled sponsored content, unverified claims, copyrighted material without rights.

### Automotive
- **Personality:** confident, engineered, aspirational, safe.
- **Best practice:** product as hero with true design lines, real driving contexts, clear specs and pricing terms.
- **Refuse:** unsafe driving depictions (speeding, no seatbelts), unsubstantiated range or mileage claims.

### Agriculture and food production
- **Personality:** grounded, honest, practical, sustainable.
- **Best practice:** real farms and farmers, local languages, practical outcomes (yield, cost, time), simple visuals that work on basic phones.
- **Refuse:** romanticised poverty, unsubstantiated yield promises, imagery from the wrong region or crop.

### Travel and hospitality
- **Personality:** inviting, warm, effortless, trustworthy.
- **Best practice:** true-to-life places and rooms, all-inclusive pricing shown clearly, a calm booking flow.
- **Refuse:** drip pricing (fees hidden until checkout), over-edited imagery, fake urgency.

### Entertainment and gaming
- **Personality:** bold, immersive, dramatic.
- **Best practice:** this is where cinematic light, epic scale, fantasy worlds and atmospheric haze belong.
- **Refuse:** generic stock aesthetics; style mismatched to the game's genre.

## Genre drift: the most common failure

Words like "cinematic", "epic", "monumental", "volumetric rays", "haze", "mist", "ethereal", "mystical", "portal", "doorway of light", "ancient stone" and "dust in the light" pull image models toward fantasy and spiritual scenes. Use them only for entertainment, gaming or festival work where that mood fits. For corporate, fintech, health and SaaS, use "contemporary, grounded, real-world, daylight, clean studio lighting, crisp, product-led, editorial".
