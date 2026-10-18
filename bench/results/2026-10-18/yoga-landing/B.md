Here is the finished `index.html`. Every placeholder is either in square brackets in the visible text (for example `[Studio Name]`) or has a `FILL:` comment next to it, so you can search for either one. I picked sensible values for the `[[FILL]]` items and listed them at the top of the CSS.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>[Studio Name] | Yoga classes for every body</title>
<meta name="description" content="[Studio Name] offers welcoming yoga classes for all levels. See the weekly schedule and book your first class.">

<!--
  PLACEHOLDERS TO REPLACE (search for "FILL" or for text in [square brackets]):
  - Studio name: "[Studio Name]" (title, header, hero, footer)
  - Address and map link, phone, WhatsApp, Instagram handle
  - Prices and currency in the Pricing section
  - Teacher names, bios and photos
  - Testimonials (marked "Placeholder quote")
  - Opening hours and weekly schedule
  - Form action URL (the booking form posts there)
  - Images: replace the .photo blocks / hero SVG with <img> tags with real alt text
-->

<style>
/* ==========================================================
   DESIGN CHOICES (edit here)
   FILL: brand colors, fonts. No brand was given, so these are defaults.
   Palette: sage mist (page), white (cards), forest (deep sections),
            ink (text), clay (single accent).
   Fonts:   headings = Georgia / serif system stack (soft, warm)
            body     = system sans stack (clean, fast, no downloads)
   Contrast (checked by calculation):
     ink on sage mist      about 12:1
     muted on sage mist    about 6:1
     white on clay         about 5.8:1
     white on forest       about 9.7:1
     clay text on white    about 5.8:1
   ========================================================== */
:root {
  --bg:        #E4EBE4;   /* sage mist: page background */
  --surface:   #FFFFFF;   /* cards, alternate sections */
  --forest:    #2F4A3C;   /* deep sections, headings accent */
  --ink:       #1F2A24;   /* main text */
  --muted:     #4A5A50;   /* secondary text */
  --clay:      #A8482C;   /* accent: buttons, links, highlights */
  --clay-dark: #8C3A22;   /* accent hover */
  --sand:      #D3C2A6;   /* placeholder photo tone */
  --moss:      #8FA58F;   /* placeholder photo tone */
  --line:      #BFCBBF;   /* hairlines */

  --font-head: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  --font-body: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

  --radius: 10px;
  --gutter: 20px;
  --maxw: 1120px;
  --tap: 48px;
}

*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 1.0625rem;
  line-height: 1.6;
}
img, svg { display: block; max-width: 100%; }
h1, h2, h3 { font-family: var(--font-head); font-weight: 600; line-height: 1.15; margin: 0; color: var(--forest); }
h1 { font-size: clamp(2.1rem, 8vw, 3.75rem); letter-spacing: -0.01em; }
h2 { font-size: clamp(1.7rem, 5.5vw, 2.5rem); }
h3 { font-size: 1.25rem; }
p { margin: 0; }
ul { margin: 0; padding: 0; list-style: none; }
a { color: var(--clay); text-underline-offset: 3px; }
a:hover { color: var(--clay-dark); }

/* Focus: always visible */
:focus-visible { outline: 3px solid var(--ink); outline-offset: 3px; border-radius: 4px; }
.on-dark :focus-visible { outline-color: #FFFFFF; }

.skip {
  position: absolute; left: 12px; top: -80px; z-index: 100;
  background: var(--ink); color: #fff; padding: 12px 16px; border-radius: 6px;
}
.skip:focus { top: 12px; }

.wrap { width: 100%; max-width: var(--maxw); margin: 0 auto; padding: 0 var(--gutter); }
section { padding: 56px 0; }
.section-head { max-width: 40rem; margin-bottom: 28px; }
.section-head p { color: var(--muted); margin-top: 10px; }
.alt { background: var(--surface); }

/* Buttons (rounded rectangles, not pills) */
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: var(--tap); padding: 0 24px;
  background: var(--clay); color: #fff;
  font: 600 1rem/1 var(--font-body);
  border: 2px solid var(--clay); border-radius: 8px;
  text-decoration: none; cursor: pointer;
}
.btn:hover { background: var(--clay-dark); border-color: var(--clay-dark); color: #fff; }
.btn-small { min-height: 44px; padding: 0 16px; font-size: 0.95rem; }
.btn-light { background: var(--bg); color: var(--ink); border-color: var(--bg); }
.btn-light:hover { background: #fff; border-color: #fff; color: var(--ink); }

/* Header */
.site-header { background: var(--bg); border-bottom: 1px solid var(--line); }
.site-header .wrap { display: flex; align-items: center; justify-content: space-between; min-height: 64px; gap: 16px; }
.brand { font-family: var(--font-head); font-weight: 700; font-size: 1.25rem; color: var(--forest); text-decoration: none; }
.nav { display: none; }
.nav a { display: inline-flex; align-items: center; min-height: 44px; padding: 0 12px; color: var(--ink); text-decoration: none; font-weight: 500; }
.nav a:hover { color: var(--clay); text-decoration: underline; }

/* Hero */
.hero { padding: 32px 0 48px; }
.hero .wrap { display: grid; gap: 28px; }
.hero-copy { display: grid; gap: 18px; align-content: center; }
.hero-copy p { font-size: 1.15rem; color: var(--muted); max-width: 32rem; }
.hero-actions { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.hero-note { font-size: 0.95rem; color: var(--muted); }
.hero-art { border-radius: var(--radius); overflow: hidden; aspect-ratio: 4 / 3; }
.hero-art svg { width: 100%; height: 100%; }

/* Placeholder photo blocks (swap for <img>) */
.photo {
  display: flex; align-items: flex-end; justify-content: flex-start;
  background: linear-gradient(160deg, var(--sand), var(--moss));
  color: var(--ink); font-size: 0.85rem; font-weight: 600;
  padding: 10px 12px; border-radius: var(--radius);
}
.photo.tall { aspect-ratio: 4 / 5; }

/* Class styles */
.cards { display: grid; gap: 16px; }
.card { background: var(--surface); border-radius: var(--radius); padding: 22px; display: grid; gap: 10px; align-content: start; border: 1px solid var(--line); }
.alt .card { background: var(--bg); border-color: transparent; }
.card p { color: var(--muted); }
.level { font-size: 0.9rem; font-weight: 600; color: var(--forest); }
.level::before { content: ""; display: inline-block; width: 10px; height: 10px; background: var(--clay); border-radius: 2px; margin-right: 8px; }

/* Schedule */
.days { display: grid; gap: 16px; }
.day { background: var(--surface); border-radius: var(--radius); padding: 18px 20px; border: 1px solid var(--line); }
.day h3 { font-size: 1.15rem; margin-bottom: 8px; }
.day li { display: grid; grid-template-columns: 5.5rem 1fr; gap: 4px 12px; padding: 10px 0; border-top: 1px solid var(--line); align-items: baseline; }
.day li:first-of-type { border-top: 0; }
.time { font-weight: 700; color: var(--ink); white-space: nowrap; }
.what small { display: block; color: var(--muted); font-size: 0.9rem; }
.schedule-foot { margin-top: 20px; color: var(--muted); font-size: 0.95rem; }

/* Teachers */
.teacher { display: grid; gap: 14px; }
.teacher p { color: var(--muted); }
.teacher .role { font-weight: 600; color: var(--clay); font-size: 0.95rem; }

/* Pricing */
.prices { display: grid; gap: 16px; }
.price { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; display: grid; gap: 8px; align-content: start; }
.price .amount { font-family: var(--font-head); font-size: 2.25rem; font-weight: 700; color: var(--forest); line-height: 1.1; }
.price .amount small { font-family: var(--font-body); font-size: 0.95rem; font-weight: 500; color: var(--muted); }
.price p { color: var(--muted); }
.price.featured { background: var(--forest); color: #fff; border-color: var(--forest); }
.price.featured h3, .price.featured .amount { color: #fff; }
.price.featured p, .price.featured .amount small { color: #E4EBE4; }
.price.featured .btn { margin-top: 10px; }
.price .tag { justify-self: start; background: var(--clay); color: #fff; font-size: 0.85rem; font-weight: 700; padding: 4px 10px; border-radius: 6px; }
.price-note { margin-top: 18px; color: var(--muted); font-size: 0.95rem; }

/* Testimonials */
.quotes { display: grid; gap: 16px; }
blockquote { margin: 0; background: var(--surface); border-left: 4px solid var(--clay); border-radius: var(--radius); padding: 22px; }
blockquote p { font-family: var(--font-head); font-size: 1.15rem; line-height: 1.45; color: var(--ink); }
blockquote footer { margin-top: 12px; color: var(--muted); font-size: 0.95rem; }
.ph-tag { display: inline-block; margin-top: 8px; font-size: 0.8rem; font-weight: 700; color: var(--muted); border: 1px dashed var(--muted); border-radius: 4px; padding: 2px 8px; }

/* CTA band */
.cta-band { background: var(--forest); color: #fff; text-align: center; }
.cta-band h2 { color: #fff; }
.cta-band p { color: #E4EBE4; margin: 12px auto 24px; max-width: 34rem; }

/* Visit and contact */
.visit { display: grid; gap: 32px; }
.contact-list { display: grid; gap: 4px; margin-top: 18px; }
.contact-list li { display: grid; gap: 2px; padding: 10px 0; border-top: 1px solid var(--line); }
.contact-list strong { font-size: 0.95rem; color: var(--forest); }
.contact-list a { display: inline-flex; align-items: center; min-height: 44px; font-weight: 600; }
address { font-style: normal; }
.hours { width: 100%; border-collapse: collapse; }
.hours th, .hours td { text-align: left; padding: 8px 0; font-weight: 400; }
.hours th { font-weight: 600; padding-right: 16px; }

form { background: var(--surface); border-radius: var(--radius); padding: 24px; display: grid; gap: 16px; border: 1px solid var(--line); }
.field { display: grid; gap: 6px; }
label { font-weight: 600; font-size: 0.95rem; }
input, select {
  width: 100%; min-height: var(--tap); padding: 10px 14px;
  font: inherit; font-size: 1rem; color: var(--ink);
  background: #fff; border: 2px solid #6F7F75; border-radius: 8px;
}
input:focus-visible, select:focus-visible { outline: 3px solid var(--ink); outline-offset: 2px; border-color: var(--ink); }
form .btn { width: 100%; }
.form-note { font-size: 0.9rem; color: var(--muted); }

/* Footer */
footer.site-footer { background: var(--ink); color: #E4EBE4; padding: 28px 0; font-size: 0.95rem; }
footer.site-footer a { color: #fff; display: inline-flex; align-items: center; min-height: 44px; }

/* Tablet and up */
@media (min-width: 700px) {
  :root { --gutter: 32px; }
  section { padding: 80px 0; }
  .cards { grid-template-columns: repeat(2, 1fr); }
  .days { grid-template-columns: repeat(2, 1fr); }
  .prices { grid-template-columns: repeat(2, 1fr); }
  .quotes { grid-template-columns: repeat(3, 1fr); }
  .teachers { grid-template-columns: repeat(3, 1fr); }
}
@media (min-width: 960px) {
  .nav { display: flex; gap: 4px; }
  .hero { padding: 64px 0 88px; }
  .hero .wrap { grid-template-columns: 1fr 1.1fr; gap: 56px; align-items: center; }
  .hero-art { aspect-ratio: 5 / 4; }
  .cards { grid-template-columns: repeat(3, 1fr); }
  .days { grid-template-columns: repeat(3, 1fr); }
  .prices { grid-template-columns: repeat(4, 1fr); }
  .visit { grid-template-columns: 1fr 1fr; gap: 56px; align-items: start; }
}
</style>
</head>

<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="#top">[Studio Name]</a> <!-- FILL: studio name -->
    <nav class="nav" aria-label="Main">
      <a href="#classes">Classes</a>
      <a href="#schedule">Schedule</a>
      <a href="#teachers">Teachers</a>
      <a href="#pricing">Pricing</a>
      <a href="#visit">Visit</a>
    </nav>
    <a class="btn btn-small" href="#book">Book a class</a>
  </div>
</header>

<main id="main">

  <!-- 1. HERO -->
  <section class="hero" id="top" aria-labelledby="hero-title">
    <div class="wrap">
      <div class="hero-copy">
        <h1 id="hero-title">[Studio Name]</h1> <!-- FILL: studio name -->
        <p>Unhurried yoga classes for every body, in the heart of [Neighbourhood].</p> <!-- FILL: promise + area -->
        <div class="hero-actions">
          <a class="btn" href="#book">Book a class</a>
          <span class="hero-note">Your first class is [offer]. No experience needed.</span> <!-- FILL: first-class offer -->
        </div>
      </div>
      <div class="hero-art">
        <!-- Placeholder hero image. FILL: replace with <img src="..." alt="Students in a sunlit yoga studio"> -->
        <svg viewBox="0 0 800 640" role="img" aria-labelledby="hero-art-title" preserveAspectRatio="xMidYMid slice">
          <title id="hero-art-title">Placeholder for a photo of the studio in morning light</title>
          <rect width="800" height="640" fill="#D3C2A6"/>
          <rect y="360" width="800" height="280" fill="#8FA58F"/>
          <circle cx="590" cy="170" r="86" fill="#E9DDC6"/>
          <path d="M0 400 Q 200 300 400 380 T 800 340 V640 H0 Z" fill="#6F8A76"/>
          <path d="M0 470 Q 220 410 440 470 T 800 450 V640 H0 Z" fill="#2F4A3C"/>
          <rect x="250" y="500" width="300" height="14" rx="7" fill="#A8482C"/>
        </svg>
      </div>
    </div>
  </section>

  <!-- 2. CLASS STYLES -->
  <section class="alt" id="classes" aria-labelledby="classes-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="classes-title">Find a class that fits</h2>
        <p>Sample class descriptions. FILL: edit to match your timetable.</p>
      </div>
      <ul class="cards">
        <li class="card">
          <h3>Vinyasa Flow</h3>
          <p>Breath-led movement that builds heat, strength and focus.</p>
          <span class="level">Level: Intermediate</span>
        </li>
        <li class="card">
          <h3>Yin and Restore</h3>
          <p>Long, quiet holds to release tension and settle the nervous system.</p>
          <span class="level">Level: All levels</span>
        </li>
        <li class="card">
          <h3>Beginners Foundations</h3>
          <p>Learn the basic shapes, props and breathing at an easy pace.</p>
          <span class="level">Level: Beginner</span>
        </li>
        <li class="card">
          <h3>Prenatal Yoga</h3>
          <p>Gentle, safe movement for every trimester, with a supportive group.</p>
          <span class="level">Level: All levels</span>
        </li>
        <li class="card">
          <h3>Morning Hatha</h3>
          <p>A steady, grounded practice to start the day with clarity.</p>
          <span class="level">Level: Beginner to intermediate</span>
        </li>
      </ul>
    </div>
  </section>

  <!-- 3. WEEKLY SCHEDULE -->
  <section id="schedule" aria-labelledby="schedule-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="schedule-title">Weekly schedule</h2>
        <p>Sample timetable. FILL: replace with your real classes and times.</p>
      </div>
      <div class="days">
        <div class="day">
          <h3>Monday</h3>
          <ul>
            <li><span class="time">7:00 am</span><span class="what">Morning Hatha<small>60 min, with [Teacher 1]</small></span></li>
            <li><span class="time">6:30 pm</span><span class="what">Vinyasa Flow<small>60 min, with [Teacher 2]</small></span></li>
          </ul>
        </div>
        <div class="day">
          <h3>Tuesday</h3>
          <ul>
            <li><span class="time">9:30 am</span><span class="what">Prenatal Yoga<small>60 min, with [Teacher 3]</small></span></li>
            <li><span class="time">7:00 pm</span><span class="what">Beginners Foundations<small>60 min, with [Teacher 1]</small></span></li>
          </ul>
        </div>
        <div class="day">
          <h3>Wednesday</h3>
          <ul>
            <li><span class="time">7:00 am</span><span class="what">Vinyasa Flow<small>60 min, with [Teacher 2]</small></span></li>
            <li><span class="time">7:30 pm</span><span class="what">Yin and Restore<small>75 min, with [Teacher 1]</small></span></li>
          </ul>
        </div>
        <div class="day">
          <h3>Thursday</h3>
          <ul>
            <li><span class="time">7:00 am</span><span class="what">Morning Hatha<small>60 min, with [Teacher 3]</small></span></li>
            <li><span class="time">6:30 pm</span><span class="what">Vinyasa Flow<small>60 min, with [Teacher 2]</small></span></li>
          </ul>
        </div>
        <div class="day">
          <h3>Friday</h3>
          <ul>
            <li><span class="time">12:15 pm</span><span class="what">Lunchtime Flow<small>45 min, with [Teacher 2]</small></span></li>
            <li><span class="time">6:00 pm</span><span class="what">Yin and Restore<small>75 min, with [Teacher 1]</small></span></li>
          </ul>
        </div>
        <div class="day">
          <h3>Saturday and Sunday</h3>
          <ul>
            <li><span class="time">Sat 9:00 am</span><span class="what">Beginners Foundations<small>60 min, with [Teacher 3]</small></span></li>
            <li><span class="time">Sat 10:30 am</span><span class="what">Prenatal Yoga<small>60 min, with [Teacher 3]</small></span></li>
            <li><span class="time">Sun 9:00 am</span><span class="what">Slow Vinyasa<small>75 min, with [Teacher 1]</small></span></li>
          </ul>
        </div>
      </div>
      <p class="schedule-foot">Arrive 10 minutes early for your first class. Mats and props are provided.</p>
    </div>
  </section>

  <!-- 4. TEACHERS -->
  <section class="alt" id="teachers" aria-labelledby="teachers-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="teachers-title">Meet your teachers</h2>
        <p>Placeholder bios. FILL: real names, photos and short bios.</p>
      </div>
      <div class="teachers cards">
        <article class="teacher">
          <div class="photo tall" role="img" aria-label="Placeholder photo of Teacher 1">Photo: [Teacher 1]</div> <!-- FILL: replace with <img> -->
          <h3>[Teacher 1 name]</h3>
          <span class="role">Vinyasa and Yin</span>
          <p>Practising for 12 years and teaching for 8. Known for clear cues and a calm, friendly room.</p>
        </article>
        <article class="teacher">
          <div class="photo tall" role="img" aria-label="Placeholder photo of Teacher 2">Photo: [Teacher 2]</div>
          <h3>[Teacher 2 name]</h3>
          <span class="role">Vinyasa and Hatha</span>
          <p>Former dancer who loves helping people find strength without strain. Great for first-timers.</p>
        </article>
        <article class="teacher">
          <div class="photo tall" role="img" aria-label="Placeholder photo of Teacher 3">Photo: [Teacher 3]</div>
          <h3>[Teacher 3 name]</h3>
          <span class="role">Prenatal and Beginners</span>
          <p>Certified prenatal teacher and mother of two. Brings patience, humour and practical tips.</p>
        </article>
      </div>
    </div>
  </section>

  <!-- 5. PRICING -->
  <section id="pricing" aria-labelledby="pricing-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="pricing-title">Simple pricing</h2>
        <p>FILL: replace the sample prices and currency below with your real ones.</p>
      </div>
      <div class="prices">
        <div class="price featured">
          <span class="tag">First class offer</span>
          <h3>Trial class</h3>
          <div class="amount">$10 <small>one time</small></div> <!-- FILL: price + currency -->
          <p>Try any class for your first visit. New students only.</p>
          <a class="btn btn-light" href="#book">Book a class</a>
        </div>
        <div class="price">
          <h3>Drop-in</h3>
          <div class="amount">$24 <small>per class</small></div> <!-- FILL -->
          <p>Pay as you go, no commitment.</p>
        </div>
        <div class="price">
          <h3>10-class pack</h3>
          <div class="amount">$200 <small>valid 4 months</small></div> <!-- FILL -->
          <p>Save $40 and use it on any class.</p>
        </div>
        <div class="price">
          <h3>Monthly unlimited</h3>
          <div class="amount">$120 <small>per month</small></div> <!-- FILL -->
          <p>Come as often as you like. Cancel any time.</p>
        </div>
      </div>
      <p class="price-note">Prices shown in [currency]. Student and concession rates available on request.</p> <!-- FILL: currency -->
    </div>
  </section>

  <!-- 6. TESTIMONIALS -->
  <section class="alt" aria-labelledby="quotes-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="quotes-title">Kind words</h2>
        <span class="ph-tag">Placeholder quotes: replace with real, permitted testimonials</span>
      </div>
      <div class="quotes">
        <blockquote>
          <p>I had never done yoga before and felt welcome from the first minute.</p>
          <footer>[Student name], beginner</footer>
          <span class="ph-tag">Placeholder quote</span>
        </blockquote>
        <blockquote>
          <p>The Wednesday yin class is the best hour of my week. I sleep better and I stress less.</p>
          <footer>[Student name], member</footer>
          <span class="ph-tag">Placeholder quote</span>
        </blockquote>
        <blockquote>
          <p>Safe, kind and well taught. The prenatal class got me through my third trimester.</p>
          <footer>[Student name], prenatal student</footer>
          <span class="ph-tag">Placeholder quote</span>
        </blockquote>
      </div>
    </div>
  </section>

  <!-- CTA BAND (second "Book a class" button) -->
  <section class="cta-band on-dark" aria-labelledby="cta-title">
    <div class="wrap">
      <h2 id="cta-title">Ready to roll out your mat?</h2>
      <p>Your first class is [offer]. Pick a class and we will save you a spot.</p> <!-- FILL: offer -->
      <a class="btn btn-light" href="#book">Book a class</a>
    </div>
  </section>

  <!-- 7. VISIT AND CONTACT -->
  <section id="visit" aria-labelledby="visit-title">
    <div class="wrap visit">
      <div>
        <h2 id="visit-title">Visit the studio</h2>
        <ul class="contact-list">
          <li>
            <strong>Address</strong>
            <address>[Street address], [City] [Postcode]</address> <!-- FILL: address -->
            <a href="https://www.google.com/maps/search/?api=1&amp;query=Your+Address+Here">Open in maps</a> <!-- FILL: map link -->
          </li>
          <li>
            <strong>Opening hours</strong>
            <table class="hours">
              <tbody>
                <tr><th scope="row">Mon to Fri</th><td>6:30 am to 8:30 pm</td></tr>
                <tr><th scope="row">Saturday</th><td>8:30 am to 1:00 pm</td></tr>
                <tr><th scope="row">Sunday</th><td>8:30 am to 12:00 pm</td></tr>
              </tbody>
            </table> <!-- FILL: hours -->
          </li>
          <li>
            <strong>Phone and WhatsApp</strong>
            <a href="tel:+10000000000">[+00 000 000 0000]</a> <!-- FILL: phone -->
            <a href="https://wa.me/10000000000">Message us on WhatsApp</a> <!-- FILL: WhatsApp number -->
          </li>
          <li>
            <strong>Instagram</strong>
            <a href="https://www.instagram.com/yourstudio/">@yourstudio</a> <!-- FILL: handle -->
          </li>
        </ul>
      </div>

      <form id="book" action="https://example.com/placeholder-booking-endpoint" method="post"> <!-- FILL: form action URL -->
        <h2 style="font-size:1.6rem">Book a class</h2>
        <div class="field">
          <label for="name">Name</label>
          <input id="name" name="name" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="phone">Phone</label>
          <input id="phone" name="phone" type="tel" autocomplete="tel" required>
        </div>
        <div class="field">
          <label for="class">Preferred class</label>
          <select id="class" name="preferred_class" required>
            <option value="" selected disabled>Choose a class</option>
            <option>Vinyasa Flow</option>
            <option>Yin and Restore</option>
            <option>Beginners Foundations</option>
            <option>Prenatal Yoga</option>
            <option>Morning Hatha</option>
            <option>Not sure yet</option>
          </select>
        </div>
        <button class="btn" type="submit">Book a class</button>
        <p class="form-note">We will confirm your spot by email or WhatsApp. Your details are only used to arrange your class.</p>
      </form>
    </div>
  </section>

</main>

<footer class="site-footer on-dark">
  <div class="wrap">
    <p>&copy; [Studio Name]. All rights reserved.</p> <!-- FILL: studio name -->
    <a href="#top">Back to top</a>
  </div>
</footer>

</body>
</html>
```

Summary:
1. Built a single-file, no-JS, mobile-first yoga landing page with all 7 sections in order, a "Book a class" button in the hero and again in a CTA band plus the booking form, inline SVG and block image placeholders, and a palette of sage, forest and ink with one clay accent.
2. Still to replace: studio name, tagline and area, class and schedule details, teacher names, bios and photos, prices and currency, testimonials (marked as placeholders), address, map link, phone, WhatsApp, Instagram, opening hours, and the form action URL.
3. Checked by calculating contrast ratios (all text AA or better) and reasoning through the layout: the hero CTA should sit near 360px down at 375px wide, with tap targets of 44 to 48px. I did not open the page in a browser here, so please check 375px and 1440px for horizontal scroll before launch.
