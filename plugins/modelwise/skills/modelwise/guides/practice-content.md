# How senior practitioners brief video, copy, research and data work

The pattern is the same everywhere: one objective, a real audience insight, one message, proof, and a check before anything ships. Use this guide for writing, research, data and video tasks. Put the parts that matter into the prompt.

Sources: TikTok creative best practices (ads.tiktok.com/help/article/creative-best-practices), Google Ads ABCDs (support.google.com/google-ads/answer/14783551), LinkedIn video ad tips (business.linkedin.com/marketing-solutions/success/best-practices/video-ad-tips), Meta Reels ads guide (facebook.com/business/ads-guide), Google Cloud's Veo 3.1 prompting guide (cloud.google.com/blog), Monzo tone of voice (monzo.com/tone-of-voice), Mailchimp content style guide, Barbara Minto's Pyramid Principle.

## Video (ads, shorts, explainers)

**The pipeline has gates.** Brief → 2–3 concept routes → script → shot list or storyboard → animatic → production → edit → versions. Changes are cheapest before production. With AI video, the animatic stage is where cheap stills and drafts belong.

What a senior producer always specifies:
1. **Objective and KPI.** One of each. Awareness leads with the brand; action leads with the product and gets more direct as it goes (Google ABCD).
2. **One proposition** and the audience insight behind it.
3. **Hook.** State the proposition in the first 3 seconds, at the latest within 6 (TikTok); reinforce the point by second 5 (LinkedIn). Hook types: a bold true claim, a visual surprise, a face mid-action, a question that names the viewer's problem.
4. **Script in two columns**, picture and audio, with each line timed. Voice-over runs at about 2.5 words per second.
5. **Shot list.** Number each shot with framing, action, on-screen text and VO line. Mark where the hook, brand, proof and CTA land.
6. **Works both muted and with sound.** TikTok and Reels are sound-on; LinkedIn is mostly muted ("think like a silent film director"). The picture plus burned-in captions must carry the message, and the audio must carry it alone. A legal line is never only in audio or only in picture.
7. **Captions and text cards.** Large, high contrast, inside safe zones, about 7 words per card at most.
8. **Brand early and throughout, ideally said aloud as well as shown** (Google). One clear CTA, reinforced by VO, on an end card held 2–3 seconds (longer if it carries a mandatory warning).
9. **Pace.** For shorts, a new visual beat every 1–3 seconds. Explainers follow problem → how it works → proof → CTA.
10. **Deliverables.** Master in 9:16 plus 4:5 and 16:9; 6, 15 and 30-second cut-downs; hook variants (change only the first 3 seconds, and make them really different); captions burned in plus an SRT file.

**Safe zones (check the platform's help page before production):**
- **Meta Reels:** 9:16, 1440×2560 recommended. Keep the top ~14%, bottom ~35% and sides ~6% clear of text and logos.
- **YouTube Shorts:** 1080×1920. Keep the top 10%, bottom 25% and right 10% clear.
- **TikTok:** 9:16, at least 720p, inside the UI safe zone.
- **LinkedIn:** 7–15 seconds suits completion; keep it under 30 for awareness.

**AI video in production:**
- Lock reference stills for character, product and setting first.
- Generate one shot per prompt, 4–8 seconds each. Veo's formula is cinematography + subject + action + context + style, with dialogue in quotes and "SFX:" and "Ambient noise:" lines. Describe what you want instead of listing negatives.
- Plan 10–25 generations per usable shot. Kalshi's widely reported Veo ad took 300–400 generations for about 15 usable clips.
- Finish by hand: edit, grade, mix and captions.
- Never generate text, logos, UI, real product footage, financial numbers or legal disclaimers in the video model. Overlay them in the edit.
- Label AI-generated content where the platform or local law requires it.

## Copywriting and content

1. **Objective** and one measurable outcome.
2. **Audience:** the job they're trying to do, the tension they feel, and the words they actually use. Not demographics.
3. **Insight → proposition.** An insight is a human truth, not a product fact. The proposition is one sentence; if it needs three, it isn't one yet.
4. **Messaging hierarchy:** the one thing → 2–3 reasons to believe → supporting detail. Cut what falls below the line.
5. **Proof:** specific, sourced, dated and permitted. Never invent statistics, testimonials, customer names or numbers. Mark gaps as `[NEEDS PROOF]`.
6. **Voice and tone.** Voice stays constant; tone shifts with the reader's situation (Mailchimp). Give "we sound like / we never sound like". Monzo turns wit down to zero in service and operational messages and up in campaigns.
7. **Specific, not adjectives.** Replace "seamless, powerful, best-in-class" with what actually happens.
8. **Headlines:** ask for 10 variants across different angles (benefit, curiosity, proof, contrast, direct), then the best 3 with a reason each. Match the headline to how aware the reader already is of the problem and the product.
9. **Review:** check against the proposition, check every claim for proof, read it aloud.
10. **Output:** the piece, 2–3 alternates only if asked, a claims-and-proof table for regulated work, and open questions.

## Research and data analysis

1. **Frame:** the decision this will change and who makes it; the question in one sentence; scope; hypotheses written down before looking.
2. **Define metrics in writing:** numerator, denominator, time grain, time zone, exclusions (test records, internal users, refunds, bots).
3. **Check data quality before analysing:** freshness, row counts against the previous period, nulls in filtered columns, duplicates and keys, allowed values. A pipeline gap looks exactly like a real drop.
4. **Analyse against a baseline or control.** Segment, reconcile totals, separate correlation from causation, run the obvious check that could prove you wrong, and quantify uncertainty.
5. **Answer first** (Pyramid Principle): one-line answer → recommendation and next step → 2–3 findings with evidence → caveats and method → appendix.
6. **Label confidence** (high, medium or low) and state what would change the conclusion.
7. **Web research:** cite every claim with a link and date, prefer primary sources, separate fact from inference, flag single-source claims.

## Industry modifiers for content and video

Every regulated piece ends with a **compliance review needed** note listing each element a human must check. The skill is not a lawyer.

**Regulated finance** (investments, lending, insurance, crypto):
- Clear, direct and kind. Explain jargon. No jokes about money worries or spending shame.
- **Mandatory lines:** used verbatim. In video they are both shown and spoken, at a pace people can follow; never speed them up to fit.
- **Never include:** invented performance figures, testimonials, rankings, or "guaranteed" and "risk-free" language.
- **Rates:** an ad that shows a rate shows its fees and terms with it.
- **Market rules:** for a category and market covered by `guides/regulated.md`, use its section; otherwise research the rules or ask for the compliance team's list.

### Banking
- Reassuring, precise, unflashy. Show fees and rates together. No guarantee language outside products that are actually guaranteed. Only use legal lines the client supplies.

### IT and B2B tech
- Name the buyer's role and their business problem, not the feature. Show the product in use within the first 10 seconds of a video.
- **Proof:** named customers, dated outcomes, real certifications. Never fabricate logos, quotes, benchmarks or certifications.
- Only about 5% of B2B buyers are in market at any time, so build distinctive, memorable brand assets as well as lead-generation pieces.

### Startups
- Plain, specific, a clear point of view, founder-credible.
- Use the proof you have (users, waitlist, pilot results, permitted customer names) and never inflate it.
- There are two valid growth routes: trust built through the product and referrals (some brokers run no paid ads at all), or high-reach advertising with humour and education.
- Sector rules still apply: a fintech startup follows the finance rules above.
