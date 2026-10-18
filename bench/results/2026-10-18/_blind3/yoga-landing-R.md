Here's a complete, single-file landing page for a fictional studio called **Stillwater Yoga**. It's plain HTML, CSS, and a little JavaScript, so there's no build step. Save it as `index.html` and open it in a browser.

**What's included**
- A sticky header with a mobile menu toggle
- A hero section with a "Book your first class free" call to action
- Philosophy and benefits
- Class cards (Vinyasa, Hatha, Yin, Prenatal, Hot Flow, Meditation)
- A weekly schedule with day tabs
- Instructor profiles
- Pricing (intro offer, class packs, unlimited membership)
- Testimonials
- A trial signup form with client-side validation
- A footer with location, hours, and contact details

**Design notes**
- The palette is earthy (sage, clay, warm cream) with Cormorant Garamond headings and Inter body text.
- It has no image dependencies. The visuals are CSS gradients and inline SVG, so nothing breaks when you deploy it. Swap in real photos wherever you see a `.photo` element.
- It's responsive down to 320px, and it respects `prefers-reduced-motion`.
- For accessibility it uses semantic landmarks, a skip link, focus styles, ARIA on the tabs and menu, and labelled form fields.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Stillwater Yoga — Breathe. Move. Belong.</title>
  <meta name="description" content="Stillwater Yoga is a warm, welcoming studio offering Vinyasa, Hatha, Yin, Prenatal and Meditation classes for every body. Your first class is free." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {
      --cream: #f7f2ea;
      --sand: #ede4d6;
      --sage: #7d8f72;
      --sage-dark: #4f5f47;
      --clay: #c07a5a;
      --clay-dark: #a3613f;
      --ink: #2c2a26;
      --muted: #6b665d;
      --white: #fffdf9;
      --radius: 18px;
      --shadow: 0 10px 30px rgba(44, 42, 38, 0.08);
      --max: 1160px;
      --serif: "Cormorant Garamond", Georgia, serif;
      --sans: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
    }

    *, *::before, *::after { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: var(--sans);
      color: var(--ink);
      background: var(--cream);
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
    }
    img, svg { display: block; max-width: 100%; }
    a { color: inherit; }
    h1, h2, h3 { font-family: var(--serif); font-weight: 600; line-height: 1.15; margin: 0 0 .5em; }
    h1 { font-size: clamp(2.6rem, 6vw, 4.6rem); }
    h2 { font-size: clamp(2rem, 4vw, 3rem); }
    h3 { font-size: 1.6rem; }
    p { margin: 0 0 1em; }

    .container { width: min(100% - 2rem, var(--max)); margin-inline: auto; }
    .section { padding: clamp(4rem, 9vw, 7rem) 0; }
    .eyebrow {
      display: inline-block;
      font-size: .78rem;
      letter-spacing: .18em;
      text-transform: uppercase;
      font-weight: 600;
      color: var(--sage-dark);
      margin-bottom: 1rem;
    }
    .lead { font-size: 1.15rem; color: var(--muted); max-width: 60ch; }
    .center { text-align: center; }
    .center .lead { margin-inline: auto; }

    .skip-link {
      position: absolute; left: -999px; top: 1rem;
      background: var(--ink); color: var(--white);
      padding: .6rem 1rem; border-radius: 8px; z-index: 100;
    }
    .skip-link:focus { left: 1rem; }
    :focus-visible { outline: 3px solid var(--clay); outline-offset: 3px; border-radius: 6px; }

    /* Buttons */
    .btn {
      display: inline-flex; align-items: center; justify-content: center; gap: .5rem;
      padding: .95rem 1.7rem;
      border-radius: 999px;
      font: 600 .95rem/1 var(--sans);
      text-decoration: none;
      border: 2px solid transparent;
      cursor: pointer;
      transition: transform .2s ease, background .2s ease, color .2s ease, border-color .2s ease;
    }
    .btn:hover { transform: translateY(-2px); }
    .btn-primary { background: var(--clay); color: var(--white); }
    .btn-primary:hover { background: var(--clay-dark); }
    .btn-ghost { border-color: var(--ink); color: var(--ink); background: transparent; }
    .btn-ghost:hover { background: var(--ink); color: var(--white); }

    /* Header */
    .site-header {
      position: sticky; top: 0; z-index: 50;
      background: rgba(247, 242, 234, .88);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border-bottom: 1px solid transparent;
      transition: border-color .3s ease;
    }
    .site-header.scrolled { border-bottom-color: var(--sand); }
    .nav { display: flex; align-items: center; justify-content: space-between; height: 76px; }
    .logo { display: flex; align-items: center; gap: .6rem; text-decoration: none; font-family: var(--serif); font-size: 1.6rem; font-weight: 600; }
    .logo svg { width: 34px; height: 34px; }
    .nav-links { display: flex; align-items: center; gap: 2rem; list-style: none; margin: 0; padding: 0; }
    .nav-links a:not(.btn) { text-decoration: none; font-size: .95rem; font-weight: 500; color: var(--muted); transition: color .2s; }
    .nav-links a:not(.btn):hover { color: var(--ink); }
    .nav-links .btn { padding: .7rem 1.3rem; }
    .menu-toggle {
      display: none; background: none; border: 0; padding: .5rem; cursor: pointer;
    }
    .menu-toggle span { display: block; width: 24px; height: 2px; background: var(--ink); margin: 5px 0; transition: transform .3s, opacity .3s; }
    .menu-toggle[aria-expanded="true"] span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
    .menu-toggle[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
    .menu-toggle[aria-expanded="true"] span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

    /* Hero */
    .hero { padding: clamp(3rem, 7vw, 6rem) 0 clamp(4rem, 8vw, 7rem); overflow: hidden; }
    .hero-grid { display: grid; grid-template-columns: 1.1fr 1fr; gap: clamp(2rem, 5vw, 5rem); align-items: center; }
    .hero h1 em { font-style: italic; color: var(--sage-dark); }
    .hero-actions { display: flex; flex-wrap: wrap; gap: 1rem; margin: 2rem 0 2.5rem; }
    .hero-stats { display: flex; gap: 2.5rem; flex-wrap: wrap; }
    .hero-stats strong { display: block; font-family: var(--serif); font-size: 2rem; line-height: 1; }
    .hero-stats span { font-size: .85rem; color: var(--muted); }
    .hero-art {
      position: relative;
      aspect-ratio: 4 / 5;
      border-radius: 200px 200px var(--radius) var(--radius);
      background:
        radial-gradient(circle at 50% 30%, #f3d9c4 0 18%, transparent 19%),
        linear-gradient(180deg, #e9c8ae 0%, #d7a585 45%, #8fa283 46%, #6f8364 100%);
      box-shadow: var(--shadow);
    }
    .hero-art svg { position: absolute; inset: auto 0 12% 0; margin: auto; width: 62%; }
    .hero-badge {
      position: absolute; left: -1.5rem; bottom: 2.5rem;
      background: var(--white); padding: 1rem 1.25rem; border-radius: 14px;
      box-shadow: var(--shadow); display: flex; align-items: center; gap: .8rem;
      font-size: .9rem;
    }
    .hero-badge .dot { width: 10px; height: 10px; border-radius: 50%; background: #6bbf6b; box-shadow: 0 0 0 4px rgba(107,191,107,.2); }

    /* Philosophy */
    .philosophy { background: var(--white); }
    .pillars { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-top: 3.5rem; }
    .pillar { padding: 2rem; border-radius: var(--radius); background: var(--cream); }
    .pillar-icon { width: 52px; height: 52px; border-radius: 50%; background: var(--sand); display: grid; place-items: center; margin-bottom: 1.2rem; }
    .pillar-icon svg { width: 26px; height: 26px; stroke: var(--sage-dark); }
    .pillar p { color: var(--muted); margin: 0; }

    /* Classes */
    .classes-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.75rem; margin-top: 3.5rem; }
    .class-card {
      background: var(--white); border-radius: var(--radius); overflow: hidden;
      box-shadow: var(--shadow); display: flex; flex-direction: column;
      transition: transform .3s ease;
    }
    .class-card:hover { transform: translateY(-6px); }
    .photo { aspect-ratio: 16 / 10; }
    .photo.p1 { background: linear-gradient(135deg, #d9a88a, #b9765a); }
    .photo.p2 { background: linear-gradient(135deg, #a8b89c, #6f8364); }
    .photo.p3 { background: linear-gradient(135deg, #c9b9d6, #8c7aa3); }
    .photo.p4 { background: linear-gradient(135deg, #f0cdb7, #d99a7c); }
    .photo.p5 { background: linear-gradient(135deg, #e8a77a, #c0583a); }
    .photo.p6 { background: linear-gradient(135deg, #b8c9cf, #6c8a94); }
    .class-body { padding: 1.6rem 1.6rem 1.8rem; display: flex; flex-direction: column; flex: 1; }
    .class-body p { color: var(--muted); font-size: .95rem; flex: 1; }
    .tags { display: flex; gap: .5rem; flex-wrap: wrap; }
    .tag { font-size: .75rem; font-weight: 600; padding: .3rem .7rem; border-radius: 999px; background: var(--sand); color: var(--sage-dark); }

    /* Schedule */
    .schedule { background: var(--sand); }
    .tabs { display: flex; gap: .5rem; flex-wrap: wrap; justify-content: center; margin: 2.5rem 0 2rem; }
    .tab {
      border: 0; background: transparent; padding: .65rem 1.2rem; border-radius: 999px;
      font: 600 .9rem var(--sans); color: var(--muted); cursor: pointer; transition: background .2s, color .2s;
    }
    .tab[aria-selected="true"] { background: var(--ink); color: var(--white); }
    .tab:hover:not([aria-selected="true"]) { background: rgba(44,42,38,.08); }
    .schedule-list { list-style: none; margin: 0 auto; padding: 0; max-width: 820px; }
    .schedule-item {
      display: grid; grid-template-columns: 110px 1fr auto auto; gap: 1.5rem; align-items: center;
      background: var(--white); padding: 1.1rem 1.5rem; border-radius: 14px; margin-bottom: .75rem;
    }
    .schedule-item time { font-weight: 600; }
    .schedule-item .cls { font-family: var(--serif); font-size: 1.3rem; font-weight: 600; }
    .schedule-item .teacher { color: var(--muted); font-size: .9rem; }
    .schedule-item .btn { padding: .55rem 1.1rem; font-size: .85rem; }

    /* Instructors */
    .team-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.75rem; margin-top: 3.5rem; }
    .member { text-align: center; }
    .avatar {
      width: 100%; aspect-ratio: 1; border-radius: 50%; margin-bottom: 1.25rem;
      display: grid; place-items: center; font-family: var(--serif); font-size: 3rem; color: var(--white);
    }
    .member h3 { font-size: 1.4rem; margin-bottom: .2rem; }
    .member .role { color: var(--clay-dark); font-weight: 600; font-size: .85rem; margin-bottom: .6rem; }
    .member p { color: var(--muted); font-size: .92rem; }

    /* Pricing */
    .pricing { background: var(--white); }
    .pricing-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.75rem; margin-top: 3.5rem; align-items: stretch; }
    .plan {
      border: 1px solid var(--sand); border-radius: var(--radius); padding: 2.4rem 2rem;
      display: flex; flex-direction: column; background: var(--cream); position: relative;
    }
    .plan.featured { background: var(--sage-dark); color: var(--white); border-color: var(--sage-dark); transform: scale(1.03); }
    .plan.featured .plan-desc, .plan.featured li { color: rgba(255,253,249,.85); }
    .plan .ribbon {
      position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
      background: var(--clay); color: var(--white); font-size: .75rem; font-weight: 600;
      padding: .35rem .9rem; border-radius: 999px; letter-spacing: .05em; white-space: nowrap;
    }
    .price { font-family: var(--serif); font-size: 3.2rem; font-weight: 600; line-height: 1; margin: .5rem 0; }
    .price small { font-family: var(--sans); font-size: .95rem; font-weight: 500; opacity: .75; }
    .plan-desc { color: var(--muted); font-size: .95rem; }
    .plan ul { list-style: none; padding: 0; margin: 1.5rem 0 2rem; flex: 1; }
    .plan li { padding: .45rem 0 .45rem 1.8rem; position: relative; color: var(--muted); font-size: .95rem; }
    .plan li::before {
      content: ""; position: absolute; left: 0; top: .85rem; width: 14px; height: 8px;
      border-left: 2px solid var(--clay); border-bottom: 2px solid var(--clay); transform: rotate(-45deg);
    }
    .plan.featured li::before { border-color: #f3c9b2; }
    .plan.featured .btn-ghost { border-color: var(--white); color: var(--white); }
    .plan.featured .btn-ghost:hover { background: var(--white); color: var(--sage-dark); }

    /* Testimonials */
    .quotes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.75rem; margin-top: 3.5rem; }
    blockquote {
      margin: 0; background: var(--white); padding: 2rem; border-radius: var(--radius); box-shadow: var(--shadow);
    }
    blockquote p { font-family: var(--serif); font-size: 1.3rem; line-height: 1.45; font-style: italic; }
    blockquote footer { font-size: .9rem; color: var(--muted); font-weight: 500; }
    .stars { color: var(--clay); letter-spacing: .15em; margin-bottom: .8rem; }

    /* CTA / Signup */
    .cta {
      background: var(--sage-dark); color: var(--white); border-radius: 28px;
      padding: clamp(2.5rem, 6vw, 4.5rem); display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center;
    }
    .cta .lead { color: rgba(255,253,249,.8); }
    .cta .eyebrow { color: #f3c9b2; }
    .signup { display: grid; gap: 1rem; }
    .field label { display: block; font-size: .85rem; font-weight: 500; margin-bottom: .35rem; }
    .field input, .field select {
      width: 100%; padding: .9rem 1.1rem; border-radius: 12px; border: 1px solid rgba(255,255,255,.25);
      background: rgba(255,255,255,.1); color: var(--white); font: 400 1rem var(--sans);
    }
    .field select option { color: var(--ink); }
    .field input::placeholder { color: rgba(255,253,249,.55); }
    .field input[aria-invalid="true"] { border-color: #f3a58a; }
    .error { color: #ffc8b4; font-size: .8rem; min-height: 1em; margin-top: .3rem; }
    .form-success { background: rgba(255,255,255,.12); padding: 1.5rem; border-radius: 14px; }

    /* Footer */
    .site-footer { padding: 4rem 0 2rem; }
    .footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr; gap: 2rem; }
    .footer-grid h4 { font-size: .8rem; letter-spacing: .15em; text-transform: uppercase; margin: 0 0 1rem; color: var(--sage-dark); }
    .footer-grid ul { list-style: none; padding: 0; margin: 0; }
    .footer-grid li, .footer-grid p { color: var(--muted); font-size: .92rem; margin-bottom: .5rem; }
    .footer-grid a { text-decoration: none; }
    .footer-grid a:hover { color: var(--ink); }
    .socials { display: flex; gap: .75rem; margin-top: 1rem; }
    .socials a { width: 40px; height: 40px; border-radius: 50%; background: var(--sand); display: grid; place-items: center; }
    .socials svg { width: 18px; height: 18px; fill: var(--ink); }
    .footer-bottom { border-top: 1px solid var(--sand); margin-top: 3rem; padding-top: 1.5rem; font-size: .85rem; color: var(--muted); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }

    /* Reveal-on-scroll */
    .reveal { opacity: 0; transform: translateY(24px); transition: opacity .8s ease, transform .8s ease; }
    .reveal.visible { opacity: 1; transform: none; }

    /* Responsive */
    @media (max-width: 980px) {
      .hero-grid, .cta { grid-template-columns: 1fr; }
      .hero-art { max-width: 420px; margin-inline: auto; width: 100%; }
      .classes-grid, .quotes { grid-template-columns: repeat(2, 1fr); }
      .team-grid { grid-template-columns: repeat(2, 1fr); }
      .pricing-grid { grid-template-columns: 1fr; max-width: 460px; margin-inline: auto; }
      .plan.featured { transform: none; }
      .footer-grid { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 820px) {
      .menu-toggle { display: block; }
      .nav-links {
        position: fixed; inset: 76px 0 auto 0; flex-direction: column; gap: 0;
        background: var(--cream); padding: 1rem 1.5rem 2rem; border-bottom: 1px solid var(--sand);
        transform: translateY(-120%); transition: transform .35s ease; visibility: hidden;
      }
      .nav-links.open { transform: none; visibility: visible; }
      .nav-links li { width: 100%; }
      .nav-links a:not(.btn) { display: block; padding: .9rem 0; font-size: 1.05rem; }
      .nav-links .btn { width: 100%; margin-top: .75rem; }
      .pillars { grid-template-columns: 1fr; }
    }
    @media (max-width: 600px) {
      .classes-grid, .quotes { grid-template-columns: 1fr; }
      .schedule-item { grid-template-columns: 1fr auto; gap: .3rem 1rem; }
      .schedule-item .teacher { grid-column: 1; }
      .schedule-item .level { display: none; }
      .schedule-item .btn { grid-column: 2; grid-row: 1 / span 3; }
      .hero-badge { left: .75rem; }
      .footer-grid { grid-template-columns: 1fr; }
    }
    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      *, *::before, *::after { transition: none !important; animation: none !important; }
      .reveal { opacity: 1; transform: none; }
    }
  </style>
</head>
<body>
  <a href="#main" class="skip-link">Skip to content</a>

  <!-- Header -->
  <header class="site-header" id="top">
    <nav class="container nav" aria-label="Primary">
      <a href="#top" class="logo" aria-label="Stillwater Yoga home">
        <svg viewBox="0 0 40 40" fill="none" aria-hidden="true">
          <circle cx="20" cy="20" r="19" stroke="#4f5f47" stroke-width="1.5"/>
          <path d="M20 9c3 5 3 10 0 15-3-5-3-10 0-15Z" fill="#7d8f72"/>
          <path d="M20 24c-4-1-8-4-10-8 5 0 8 3 10 8Zm0 0c4-1 8-4 10-8-5 0-8 3-10 8Z" fill="#c07a5a"/>
          <path d="M11 29c6 2 12 2 18 0" stroke="#4f5f47" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        Stillwater
      </a>
      <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="nav-links">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-links" id="nav-links">
        <li><a href="#classes">Classes</a></li>
        <li><a href="#schedule">Schedule</a></li>
        <li><a href="#teachers">Teachers</a></li>
        <li><a href="#pricing">Pricing</a></li>
        <li><a href="#trial" class="btn btn-primary">Free first class</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <!-- Hero -->
    <section class="hero">
      <div class="container hero-grid">
        <div class="reveal">
          <span class="eyebrow">Yoga &amp; meditation studio · Portland, OR</span>
          <h1>Breathe deeper.<br/>Move <em>freely.</em><br/>Find your still.</h1>
          <p class="lead">A warm, light-filled space for every body and every level. Whether it's your first downward dog or your thousandth, there's a mat waiting for you.</p>
          <div class="hero-actions">
            <a href="#trial" class="btn btn-primary">Book your first class free</a>
            <a href="#schedule" class="btn btn-ghost">View schedule</a>
          </div>
          <div class="hero-stats">
            <div><strong>40+</strong><span>classes weekly</span></div>
            <div><strong>12</strong><span>certified teachers</span></div>
            <div><strong>4.9★</strong><span>from 600+ reviews</span></div>
          </div>
        </div>
        <div class="hero-art reveal" role="img" aria-label="Illustration of a person meditating at sunset">
          <svg viewBox="0 0 200 160" fill="none" aria-hidden="true">
            <circle cx="100" cy="28" r="16" fill="#2c2a26"/>
            <path d="M100 46c-14 0-22 10-24 30l-2 22h52l-2-22c-2-20-10-30-24-30Z" fill="#2c2a26"/>
            <path d="M78 70c-10 8-22 18-26 30 8 2 18-2 28-12M122 70c10 8 22 18 26 30-8 2-18-2-28-12" stroke="#2c2a26" stroke-width="9" stroke-linecap="round"/>
            <path d="M30 118c20-14 50-20 70-20s50 6 70 20c-20 10-48 14-70 14s-50-4-70-14Z" fill="#2c2a26"/>
            <ellipse cx="100" cy="142" rx="88" ry="8" fill="#4f5f47" opacity=".5"/>
          </svg>
          <div class="hero-badge">
            <span class="dot" aria-hidden="true"></span>
            <div><strong>Next class: 6:00 pm</strong><br/><span style="color:var(--muted)">Slow Flow · 4 spots left</span></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Philosophy -->
    <section class="section philosophy" id="about">
      <div class="container center">
        <span class="eyebrow">Our philosophy</span>
        <h2>Yoga that meets you where you are</h2>
        <p class="lead">We started Stillwater in 2016 with a simple idea: yoga should feel like coming home. No mirrors, no pressure, no perfect poses. Just thoughtful teaching, real community, and room to breathe.</p>
        <div class="pillars">
          <div class="pillar reveal">
            <div class="pillar-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-4.5-7-11a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 6.5-7 11-7 11Z"/></svg></div>
            <h3>Every body welcome</h3>
            <p>Every class offers modifications and props, so you can practise safely at any age, size, or ability.</p>
          </div>
          <div class="pillar reveal">
            <div class="pillar-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg></div>
            <h3>Expert teachers</h3>
            <p>All of our teachers are 500-hour certified, with specialisms from trauma-informed yoga to pre- and postnatal practice.</p>
          </div>
          <div class="pillar reveal">
            <div class="pillar-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3-8 4 16 3-8h4"/></svg></div>
            <h3>Small classes</h3>
            <p>Classes are capped at 18 students, so you get real attention, hands-on adjustments (only if you want them), and a teacher who knows your name.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Classes -->
    <section class="section" id="classes">
      <div class="container">
        <div class="center">
          <span class="eyebrow">Classes</span>
          <h2>Find your flow</h2>
          <p class="lead">From energising vinyasa to deeply restful yin, choose the practice that fits your day.</p>
        </div>
        <div class="classes-grid">
          <article class="class-card reveal">
            <div class="photo p1" role="img" aria-label="Vinyasa class"></div>
            <div class="class-body">
              <h3>Vinyasa Flow</h3>
              <p>Breath-linked movement that builds heat, strength, and focus. Expect creative sequencing and a great playlist.</p>
              <div class="tags"><span class="tag">60 min</span><span class="tag">All levels</span></div>
            </div>
          </article>
          <article class="class-card reveal">
            <div class="photo p2" role="img" aria-label="Hatha class"></div>
            <div class="class-body">
              <h3>Hatha Foundations</h3>
              <p>Slower-paced and alignment-focused. Ideal if you're new to yoga or want to refine the fundamentals.</p>
              <div class="tags"><span class="tag">60 min</span><span class="tag">Beginner</span></div>
            </div>
          </article>
          <article class="class-card reveal">
            <div class="photo p3" role="img" aria-label="Yin class"></div>
            <div class="class-body">
              <h3>Yin &amp; Restore</h3>
              <p>Long, supported holds that release deep tension and calm the nervous system. Perfect after a long week.</p>
              <div class="tags"><span class="tag">75 min</span><span class="tag">All levels</span></div>
            </div>
          </article>
          <article class="class-card reveal">
            <div class="photo p4" role="img" aria-label="Prenatal class"></div>
            <div class="class-body">
              <h3>Prenatal Yoga</h3>
              <p>Gentle, supportive movement and breathwork for every trimester, led by a certified prenatal specialist.</p>
              <div class="tags"><span class="tag">60 min</span><span class="tag">Prenatal</span></div>
            </div>
          </article>
          <article class="class-card reveal">
            <div class="photo p5" role="img" aria-label="Hot flow class"></div>
            <div class="class-body">
              <h3>Hot Flow</h3>
              <p>Vinyasa in a room warmed to 95°F. You'll sweat, detox, and leave feeling brand new. Bring water!</p>
              <div class="tags"><span class="tag">60 min</span><span class="tag">Intermediate</span></div>
            </div>
          </article>
          <article class="class-card reveal">
            <div class="photo p6" role="img" aria-label="Meditation class"></div>
            <div class="class-body">
              <h3>Breath &amp; Meditation</h3>
              <p>Guided pranayama and meditation to quiet the mind. No experience needed, and no flexibility required.</p>
              <div class="tags"><span class="tag">45 min</span><span class="tag">All levels</span></div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Schedule -->
    <section class="section schedule" id="schedule">
      <div class="container">
        <div class="center">
          <span class="eyebrow">This week</span>
          <h2>Class schedule</h2>
          <p class="lead">Early mornings, lunch breaks, and evenings: we've got a time that works for you.</p>
        </div>
        <div class="tabs" role="tablist" aria-label="Days of the week" id="day-tabs"></div>
        <ul class="schedule-list" id="schedule-list" role="tabpanel" aria-live="polite"></ul>
      </div>
    </section>

    <!-- Teachers -->
    <section class="section" id="teachers">
      <div class="container">
        <div class="center">
          <span class="eyebrow">Our teachers</span>
          <h2>Guides for your practice</h2>
          <p class="lead">Experienced, kind, and genuinely passionate about helping you grow.</p>
        </div>
        <div class="team-grid">
          <div class="member reveal">
            <div class="avatar" style="background:linear-gradient(135deg,#c07a5a,#8e4f33)" aria-hidden="true">M</div>
            <h3>Maya Chen</h3>
            <div class="role">Founder · Vinyasa</div>
            <p>18 years of practice, trained in Mysore. She's known for playful, powerful flows.</p>
          </div>
          <div class="member reveal">
            <div class="avatar" style="background:linear-gradient(135deg,#7d8f72,#4f5f47)" aria-hidden="true">D</div>
            <h3>Daniel Ortiz</h3>
            <div class="role">Hatha · Alignment</div>
            <p>A former physiotherapist who makes anatomy approachable and keeps every pose safe.</p>
          </div>
          <div class="member reveal">
            <div class="avatar" style="background:linear-gradient(135deg,#9d8ab5,#6c5a86)" aria-hidden="true">P</div>
            <h3>Priya Nair</h3>
            <div class="role">Yin · Meditation</div>
            <p>Brings calm, deep presence to every class. Her Sunday yin sells out weekly.</p>
          </div>
          <div class="member reveal">
            <div class="avatar" style="background:linear-gradient(135deg,#d99a7c,#b26f50)" aria-hidden="true">S</div>
            <h3>Sarah Lindqvist</h3>
            <div class="role">Prenatal · Postnatal</div>
            <p>A certified doula and mother of two, she supports parents through every stage.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section class="section pricing" id="pricing">
      <div class="container">
        <div class="center">
          <span class="eyebrow">Pricing</span>
          <h2>Simple, flexible plans</h2>
          <p class="lead">No sign-up fees and no long contracts. Pause or cancel anytime.</p>
        </div>
        <div class="pricing-grid">
          <div class="plan reveal">
            <h3>New Student</h3>
            <p class="plan-desc">The perfect way to explore.</p>
            <div class="price">$49 <small>/ 30 days</small></div>
            <ul>
              <li>Unlimited classes for 30 days</li>
              <li>Free mat &amp; towel rental</li>
              <li>One welcome session with a teacher</li>
            </ul>
            <a href="#trial" class="btn btn-ghost">Start intro month</a>
          </div>
          <div class="plan featured reveal">
            <span class="ribbon">MOST POPULAR</span>
            <h3>Unlimited</h3>
            <p class="plan-desc">For a steady, regular practice.</p>
            <div class="price">$139 <small>/ month</small></div>
            <ul>
              <li>Unlimited classes, all styles</li>
              <li>Priority booking (7 days ahead)</li>
              <li>2 guest passes every month</li>
              <li>15% off workshops &amp; retail</li>
            </ul>
            <a href="#trial" class="btn btn-primary">Become a member</a>
          </div>
          <div class="plan reveal">
            <h3>Class Pack</h3>
            <p class="plan-desc">Practise on your schedule.</p>
            <div class="price">$170 <small>/ 10 classes</small></div>
            <ul>
              <li>Valid for 6 months</li>
              <li>Shareable with a friend</li>
              <li>Drop-ins also available at $22</li>
            </ul>
            <a href="#trial" class="btn btn-ghost">Buy a pack</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="section" id="reviews">
      <div class="container">
        <div class="center">
          <span class="eyebrow">Kind words</span>
          <h2>What our community says</h2>
        </div>
        <div class="quotes">
          <blockquote class="reveal">
            <div class="stars" aria-label="5 out of 5 stars">★★★★★</div>
            <p>“I was terrified of my first class. By the end I was close to tears in the best way. This place genuinely changed my year.”</p>
            <footer>Jordan K. · Member since 2022</footer>
          </blockquote>
          <blockquote class="reveal">
            <div class="stars" aria-label="5 out of 5 stars">★★★★★</div>
            <p>“The teachers actually know their stuff. My back pain is gone and I sleep better than I have in a decade.”</p>
            <footer>Elena R. · Member since 2019</footer>
          </blockquote>
          <blockquote class="reveal">
            <div class="stars" aria-label="5 out of 5 stars">★★★★★</div>
            <p>“Prenatal yoga with Sarah was the highlight of my pregnancy. Now I bring my baby to the postnatal class!”</p>
            <footer>Amara T. · Member since 2023</footer>
          </blockquote>
        </div>
      </div>
    </section>

    <!-- CTA / Trial signup -->
    <section class="section" id="trial" style="padding-top:0">
      <div class="container">
        <div class="cta">
          <div>
            <span class="eyebrow">Your first class is on us</span>
            <h2>Roll out your mat with us this week</h2>
            <p class="lead">Tell us a little about yourself and we'll reserve a spot in your first class, completely free. Mats, props, and a warm welcome are included.</p>
          </div>
          <form class="signup" id="signup-form" novalidate>
            <div class="field">
              <label for="name">Full name</label>
              <input id="name" name="name" type="text" autocomplete="name" placeholder="Your name" required />
              <div class="error" id="name-error"></div>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <input id="email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required />
              <div class="error" id="email-error"></div>
            </div>
            <div class="field">
              <label for="interest">I'm most interested in</label>
              <select id="interest" name="interest">
                <option>Not sure yet: help me choose</option>
                <option>Vinyasa Flow</option>
                <option>Hatha Foundations</option>
                <option>Yin &amp; Restore</option>
                <option>Prenatal Yoga</option>
                <option>Hot Flow</option>
                <option>Breath &amp; Meditation</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary">Claim my free class</button>
          </form>
        </div>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a href="#top" class="logo" style="margin-bottom:1rem">Stillwater Yoga</a>
          <p>A community yoga studio in the heart of Portland. Breathe. Move. Belong.</p>
          <div class="socials">
            <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4ZM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4ZM12 2c-2.7 0-3 0-4.1.1C4.3 2.3 2.3 4.3 2.1 7.9 2 9 2 9.3 2 12s0 3 .1 4.1c.2 3.6 2.2 5.6 5.8 5.8 1.1.1 1.4.1 4.1.1s3 0 4.1-.1c3.6-.2 5.6-2.2 5.8-5.8.1-1.1.1-1.4.1-4.1s0-3-.1-4.1c-.2-3.6-2.2-5.6-5.8-5.8C15 2 14.7 2 12 2Z"/></svg></a>
            <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.3V10H7v4h3v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5Z"/></svg></a>
            <a href="#" aria-label="YouTube"><svg viewBox="0 0 24 24"><path d="M22 8.2c-.2-1.5-1-2.6-2.6-2.8C17 5 12 5 12 5s-5 0-7.4.4C3 5.6 2.2 6.7 2 8.2 1.8 9.5 1.8 12 1.8 12s0 2.5.2 3.8c.2 1.5 1 2.6 2.6 2.8C7 19 12 19 12 19s5 0 7.4-.4c1.6-.2 2.4-1.3 2.6-2.8.2-1.3.2-3.8.2-3.8s0-2.5-.2-3.8ZM10 15V9l5.2 3L10 15Z"/></svg></a>
          </div>
        </div>
        <div>
          <h4>Visit</h4>
          <p>1420 SE Hawthorne Blvd<br/>Portland, OR 97214</p>
          <p><a href="https://maps.google.com/?q=1420+SE+Hawthorne+Blvd+Portland+OR" target="_blank" rel="noopener">Get directions →</a></p>
        </div>
        <div>
          <h4>Hours</h4>
          <ul>
            <li>Mon–Fri: 6:00am – 9:00pm</li>
            <li>Sat: 7:30am – 6:00pm</li>
            <li>Sun: 8:00am – 5:00pm</li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li><a href="tel:+15035550142">(503) 555-0142</a></li>
            <li><a href="mailto:hello@stillwateryoga.com">hello@stillwateryoga.com</a></li>
            <li><a href="#trial">Book a free class</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span id="year"></span> Stillwater Yoga. All rights reserved.</span>
        <span>Made with breath &amp; intention.</span>
      </div>
    </div>
  </footer>

  <script>
    // Mobile menu
    const toggle = document.querySelector('.menu-toggle');
    const links = document.getElementById('nav-links');
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      links.classList.toggle('open', !open);
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      links.classList.remove('open');
    }));

    // Header border on scroll
    const header = document.querySelector('.site-header');
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 10);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // Schedule data
    const schedule = {
      Mon: [['6:30 am','Vinyasa Flow','Maya','All levels'],['12:15 pm','Hatha Foundations','Daniel','Beginner'],['6:00 pm','Hot Flow','Maya','Intermediate'],['7:30 pm','Yin & Restore','Priya','All levels']],
      Tue: [['7:00 am','Breath & Meditation','Priya','All levels'],['12:15 pm','Vinyasa Flow','Daniel','All levels'],['5:30 pm','Prenatal Yoga','Sarah','Prenatal'],['7:00 pm','Hatha Foundations','Daniel','Beginner']],
      Wed: [['6:30 am','Hot Flow','Maya','Intermediate'],['12:15 pm','Yin & Restore','Priya','All levels'],['6:00 pm','Vinyasa Flow','Maya','All levels'],['7:30 pm','Breath & Meditation','Priya','All levels']],
      Thu: [['7:00 am','Hatha Foundations','Daniel','Beginner'],['12:15 pm','Hot Flow','Maya','Intermediate'],['5:30 pm','Prenatal Yoga','Sarah','Prenatal'],['7:00 pm','Vinyasa Flow','Daniel','All levels']],
      Fri: [['6:30 am','Vinyasa Flow','Maya','All levels'],['12:15 pm','Breath & Meditation','Priya','All levels'],['5:30 pm','Yin & Restore','Priya','All levels']],
      Sat: [['8:00 am','Hot Flow','Maya','Intermediate'],['9:30 am','Vinyasa Flow','Daniel','All levels'],['11:00 am','Hatha Foundations','Daniel','Beginner'],['1:00 pm','Postnatal (with baby)','Sarah','Postnatal']],
      Sun: [['9:00 am','Vinyasa Flow','Maya','All levels'],['11:00 am','Yin & Restore','Priya','All levels'],['4:00 pm','Breath & Meditation','Priya','All levels']]
    };
    const days = Object.keys(schedule);
    const tabsEl = document.getElementById('day-tabs');
    const listEl = document.getElementById('schedule-list');
    const todayIdx = (new Date().getDay() + 6) % 7; // Monday = 0

    function renderDay(day) {
      tabsEl.querySelectorAll('.tab').forEach(t => {
        const active = t.dataset.day === day;
        t.setAttribute('aria-selected', String(active));
        t.tabIndex = active ? 0 : -1;
      });
      listEl.setAttribute('aria-labelledby', 'tab-' + day);
      listEl.innerHTML = schedule[day].map(([time, cls, teacher, level]) => `
        <li class="schedule-item">
          <time>${time}</time>
          <div><div class="cls">${cls}</div><div class="teacher">with ${teacher}</div></div>
          <span class="tag level">${level}</span>
          <a href="#trial" class="btn btn-ghost" aria-label="Book ${cls} at ${time}">Book</a>
        </li>`).join('');
    }

    days.forEach((day, i) => {
      const btn = document.createElement('button');
      btn.className = 'tab';
      btn.id = 'tab-' + day;
      btn.type = 'button';
      btn.role = 'tab';
      btn.setAttribute('aria-controls', 'schedule-list');
      btn.dataset.day = day;
      btn.textContent = i === todayIdx ? `${day} · Today` : day;
      btn.addEventListener('click', () => renderDay(day));
      btn.addEventListener('keydown', e => {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        const next = (i + (e.key === 'ArrowRight' ? 1 : -1) + days.length) % days.length;
        renderDay(days[next]);
        tabsEl.children[next].focus();
      });
      tabsEl.appendChild(btn);
    });
    renderDay(days[todayIdx]);

    // Signup form validation
    const form = document.getElementById('signup-form');
    form.addEventListener('submit', e => {
      e.preventDefault();
      const name = form.name.value.trim();
      const email = form.email.value.trim();
      let valid = true;

      const setError = (field, msg) => {
        document.getElementById(field + '-error').textContent = msg;
        form[field].setAttribute('aria-invalid', msg ? 'true' : 'false');
        if (msg) valid = false;
      };
      setError('name', name ? '' : 'Please tell us your name.');
      setError('email', /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? '' : 'Please enter a valid email address.');

      if (!valid) { form.querySelector('[aria-invalid="true"]').focus(); return; }

      // TODO: send to your booking system / email service here (e.g. fetch('/api/trial', {...}))
      form.innerHTML = `
        <div class="form-success" role="status">
          <h3 style="margin-bottom:.4rem">Namaste, ${name.split(' ')[0].replace(/[<>&"]/g, '')}! 🙏</h3>
          <p style="margin:0">Your free class is reserved. We've sent the details to <strong>${email.replace(/[<>&"]/g, '')}</strong>. See you on the mat.</p>
        </div>`;
    });

    // Reveal on scroll
    const io = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('visible'); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12 }) : null;
    document.querySelectorAll('.reveal').forEach(el => io ? io.observe(el) : el.classList.add('visible'));

    document.getElementById('year').textContent = new Date().getFullYear();
  </script>
</body>
</html>
```

**Making it yours**
1. **Branding:** Change the studio name, logo SVG, and the color variables in `:root` at the top of the CSS.
2. **Photos:** Replace each `.photo` and `.avatar` gradient with a real image. For example, `<img src="vinyasa.jpg" alt="Students in a vinyasa class" class="photo">` works with the existing `aspect-ratio` sizing. The hero art can take a background image too.
3. **Schedule:** Edit the `schedule` object in the script. Each entry is `[time, class, teacher, level]`.
4. **Booking:** The form currently only shows a success message. Connect it to your booking platform (Mindbody, Momence, Acuity), a form service (Formspree, Netlify Forms), or your own API at the `TODO` comment. You could also point the "Book" buttons straight at your booking platform's links.
5. **Details:** Update the address, hours, phone, email, prices, and social links. The testimonials are placeholders, so replace them with real reviews before going live.

If you'd like, I can also:
- Convert this to React, Next.js, or Astro
- Add a real photo layout
- Add an FAQ or workshops section
- Add SEO structured data (`LocalBusiness`/`ExerciseGym` schema) so the studio shows up better in local search
