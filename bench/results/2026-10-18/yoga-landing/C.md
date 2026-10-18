I've built a single-file landing page for a yoga studio. I picked a name (Stillwater Yoga), a calm earthy palette, and sample classes, prices and testimonials. Replace all of these with your real details. Save it as `index.html` and open it in a browser. It has no dependencies beyond Google Fonts, and it works on phones.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Stillwater Yoga | Find your breath, find your balance</title>
  <meta name="description" content="Stillwater Yoga is a welcoming neighborhood studio offering vinyasa, yin, restorative and beginner classes. Your first week is free.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #faf6f0;
      --bg-alt: #f1e9dd;
      --ink: #2b2a27;
      --muted: #6b665d;
      --sage: #6f8a74;
      --sage-dark: #53705a;
      --clay: #c97f5f;
      --card: #ffffff;
      --line: #e3d9c9;
      --radius: 18px;
      --serif: "Fraunces", Georgia, serif;
      --sans: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #1b1d1a;
        --bg-alt: #232622;
        --ink: #efeae1;
        --muted: #a7a398;
        --sage: #8fae95;
        --sage-dark: #a9c6ae;
        --clay: #e09a7b;
        --card: #2a2d29;
        --line: #3a3e38;
      }
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: var(--sans);
      background: var(--bg);
      color: var(--ink);
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
    }
    img, svg { max-width: 100%; display: block; }
    a { color: inherit; }
    .wrap { width: min(1120px, 100% - 40px); margin-inline: auto; }
    h1, h2, h3 { font-family: var(--serif); font-weight: 500; line-height: 1.15; letter-spacing: -0.01em; }
    h2 { font-size: clamp(1.8rem, 4vw, 2.6rem); }
    .eyebrow {
      text-transform: uppercase; letter-spacing: .16em; font-size: .75rem;
      font-weight: 600; color: var(--clay); margin-bottom: 14px;
    }
    .lead { color: var(--muted); font-size: 1.1rem; max-width: 56ch; }
    section { padding: clamp(64px, 9vw, 112px) 0; }
    .section-head { margin-bottom: 48px; }
    .section-head .lead { margin-top: 14px; }

    .btn {
      display: inline-block; padding: 14px 28px; border-radius: 999px;
      font-weight: 600; font-size: .95rem; text-decoration: none;
      border: 2px solid transparent; transition: transform .15s, background .2s, color .2s;
      cursor: pointer; font-family: inherit;
    }
    .btn:hover { transform: translateY(-2px); }
    .btn:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, summary:focus-visible {
      outline: 3px solid var(--clay); outline-offset: 3px;
    }
    .btn-primary { background: var(--sage-dark); color: #fff; }
    .btn-primary:hover { background: var(--sage); }
    .btn-ghost { border-color: var(--ink); color: var(--ink); }
    .btn-ghost:hover { background: var(--ink); color: var(--bg); }

    /* Nav */
    header {
      position: sticky; top: 0; z-index: 20;
      background: color-mix(in srgb, var(--bg) 88%, transparent);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--line);
    }
    .nav { display: flex; align-items: center; justify-content: space-between; height: 70px; }
    .logo { font-family: var(--serif); font-size: 1.4rem; text-decoration: none; display: flex; align-items: center; gap: 10px; }
    .logo svg { width: 28px; height: 28px; color: var(--sage); }
    .nav ul { display: flex; gap: 30px; list-style: none; align-items: center; }
    .nav ul a { text-decoration: none; font-size: .95rem; color: var(--muted); transition: color .2s; }
    .nav ul a:hover { color: var(--ink); }
    .nav .btn { padding: 10px 20px; color: #fff; }
    .nav ul a.btn:hover { color: #fff; }
    @media (max-width: 760px) { .nav ul li:not(:last-child) { display: none; } }

    /* Hero */
    .hero { padding: clamp(56px, 8vw, 104px) 0 clamp(64px, 9vw, 120px); overflow: hidden; }
    .hero-grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: 56px; align-items: center; }
    .hero h1 { font-size: clamp(2.6rem, 6.5vw, 4.6rem); margin-bottom: 22px; }
    .hero h1 em { font-style: italic; color: var(--sage-dark); }
    .hero .lead { margin-bottom: 34px; }
    .hero-cta { display: flex; flex-wrap: wrap; gap: 14px; }
    .hero-meta { margin-top: 36px; display: flex; gap: 28px; flex-wrap: wrap; color: var(--muted); font-size: .9rem; }
    .hero-meta strong { display: block; color: var(--ink); font-family: var(--serif); font-size: 1.6rem; font-weight: 500; }
    .hero-art {
      aspect-ratio: 4/5; border-radius: 200px 200px var(--radius) var(--radius);
      background:
        radial-gradient(circle at 50% 28%, #f3d9b8 0 14%, transparent 14.5%),
        linear-gradient(180deg, #e8d3b6 0%, #d8b99a 38%, #a9bfa8 38.1%, #6f8a74 100%);
      position: relative; overflow: hidden;
    }
    .hero-art svg { position: absolute; inset: auto 0 0 0; width: 100%; height: auto; color: #3f5646; }
    @media (max-width: 860px) {
      .hero-grid { grid-template-columns: 1fr; }
      .hero-art { max-width: 380px; aspect-ratio: 4/4.4; margin-inline: auto; }
    }

    /* Classes */
    .alt { background: var(--bg-alt); }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 22px; }
    .card {
      background: var(--card); border: 1px solid var(--line); border-radius: var(--radius);
      padding: 30px 26px; transition: transform .2s, box-shadow .2s;
    }
    .card:hover { transform: translateY(-4px); box-shadow: 0 14px 34px rgba(60, 50, 30, .12); }
    .card .icon {
      width: 48px; height: 48px; border-radius: 14px; display: grid; place-items: center;
      background: color-mix(in srgb, var(--sage) 20%, transparent); color: var(--sage-dark); margin-bottom: 20px;
    }
    .card .icon svg { width: 26px; height: 26px; }
    .card h3 { font-size: 1.35rem; margin-bottom: 8px; }
    .card p { color: var(--muted); font-size: .95rem; }
    .tag {
      display: inline-block; margin-top: 16px; font-size: .75rem; font-weight: 600;
      padding: 4px 12px; border-radius: 999px; background: var(--bg-alt); color: var(--muted);
    }

    /* Schedule */
    .schedule { border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; background: var(--card); }
    .schedule table { width: 100%; border-collapse: collapse; }
    .schedule th, .schedule td { padding: 16px 20px; text-align: left; font-size: .95rem; }
    .schedule thead { background: var(--sage-dark); color: #fff; }
    .schedule th { font-weight: 600; font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; }
    .schedule tbody tr + tr { border-top: 1px solid var(--line); }
    .schedule td:first-child { font-weight: 600; white-space: nowrap; }
    .schedule td small { color: var(--muted); }
    .scroll-x { overflow-x: auto; }
    .schedule table { min-width: 560px; }

    /* About */
    .about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; }
    .about-art {
      aspect-ratio: 1; border-radius: var(--radius);
      background: linear-gradient(135deg, var(--sage) 0%, #b7c9b3 55%, #ecd9bd 100%);
      display: grid; place-items: center; color: rgba(255,255,255,.9);
    }
    .about-art svg { width: 46%; }
    .about p + p { margin-top: 16px; }
    .about p { color: var(--muted); }
    .checks { list-style: none; margin-top: 26px; display: grid; gap: 12px; }
    .checks li { display: flex; gap: 12px; align-items: flex-start; }
    .checks svg { flex: none; width: 22px; height: 22px; color: var(--sage-dark); margin-top: 3px; }
    @media (max-width: 860px) { .about-grid { grid-template-columns: 1fr; gap: 36px; } .about-art { max-width: 340px; } }

    /* Pricing */
    .pricing { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 22px; align-items: stretch; }
    .plan {
      background: var(--card); border: 1px solid var(--line); border-radius: var(--radius);
      padding: 34px 28px; display: flex; flex-direction: column; position: relative;
    }
    .plan.featured { border: 2px solid var(--sage-dark); box-shadow: 0 16px 40px rgba(83, 112, 90, .18); }
    .plan .badge {
      position: absolute; top: -13px; left: 28px; background: var(--clay); color: #fff;
      font-size: .72rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
      padding: 4px 12px; border-radius: 999px;
    }
    .plan h3 { font-size: 1.3rem; }
    .price { font-family: var(--serif); font-size: 3rem; margin: 14px 0 4px; line-height: 1; }
    .price span { font-family: var(--sans); font-size: .9rem; color: var(--muted); }
    .plan .note { color: var(--muted); font-size: .9rem; margin-bottom: 22px; }
    .plan ul { list-style: none; display: grid; gap: 10px; margin-bottom: 28px; font-size: .95rem; flex: 1; }
    .plan li::before { content: "\2713"; color: var(--sage-dark); font-weight: 700; margin-right: 10px; }
    .plan .btn { text-align: center; }

    /* Testimonials */
    .quotes { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 22px; }
    figure.quote { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 30px; }
    figure.quote blockquote { font-family: var(--serif); font-size: 1.15rem; line-height: 1.5; margin-bottom: 20px; }
    figure.quote figcaption { color: var(--muted); font-size: .9rem; }
    .stars { color: var(--clay); letter-spacing: 3px; margin-bottom: 14px; }

    /* FAQ */
    .faq { max-width: 760px; margin-inline: auto; }
    details { border-bottom: 1px solid var(--line); padding: 20px 4px; }
    summary { cursor: pointer; font-weight: 600; list-style: none; display: flex; justify-content: space-between; gap: 20px; }
    summary::-webkit-details-marker { display: none; }
    summary::after { content: "+"; font-size: 1.5rem; line-height: 1; color: var(--sage-dark); transition: transform .2s; }
    details[open] summary::after { transform: rotate(45deg); }
    details p { color: var(--muted); margin-top: 12px; }

    /* CTA / form */
    .cta {
      background: linear-gradient(135deg, var(--sage-dark), #3f5646);
      color: #fff; border-radius: 28px; padding: clamp(40px, 7vw, 80px);
      display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center;
    }
    .cta h2 { margin-bottom: 14px; }
    .cta p { color: rgba(255,255,255,.82); }
    form { display: grid; gap: 14px; }
    label { font-size: .85rem; font-weight: 600; display: grid; gap: 6px; }
    input, select {
      font: inherit; padding: 13px 16px; border-radius: 12px; border: 2px solid transparent;
      background: #fff; color: #2b2a27; width: 100%;
    }
    form .btn { background: var(--clay); color: #fff; margin-top: 6px; }
    form .btn:hover { background: #b46d4f; }
    .form-note { font-size: .8rem; color: rgba(255,255,255,.7); }
    #thanks { display: none; background: rgba(255,255,255,.14); padding: 22px; border-radius: 14px; }
    @media (max-width: 860px) { .cta { grid-template-columns: 1fr; gap: 32px; } }

    /* Footer */
    footer { padding: 56px 0 36px; border-top: 1px solid var(--line); margin-top: 96px; }
    .foot-grid { display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 36px; }
    footer h4 { font-size: .8rem; text-transform: uppercase; letter-spacing: .12em; color: var(--muted); margin-bottom: 14px; }
    footer p, footer li { color: var(--muted); font-size: .95rem; }
    footer ul { list-style: none; display: grid; gap: 8px; }
    footer a { text-decoration: none; }
    footer a:hover { color: var(--ink); }
    .copy { margin-top: 40px; font-size: .85rem; color: var(--muted); }
    @media (max-width: 760px) { .foot-grid { grid-template-columns: 1fr; } }

    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      * { transition: none !important; }
    }
  </style>
</head>
<body>

<header>
  <div class="wrap nav">
    <a href="#top" class="logo" aria-label="Stillwater Yoga home">
      <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
        <path d="M16 4c3 4 5 7 5 11a5 5 0 0 1-10 0c0-4 2-7 5-11z"/>
        <path d="M4 22c4 0 8 2 12 6 4-4 8-6 12-6"/>
      </svg>
      Stillwater
    </a>
    <nav aria-label="Main">
      <ul>
        <li><a href="#classes">Classes</a></li>
        <li><a href="#schedule">Schedule</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#pricing">Pricing</a></li>
        <li><a href="#join" class="btn btn-primary">Free first week</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="top">

  <!-- HERO -->
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">Neighborhood yoga studio</p>
        <h1>Find your breath. <em>Find your balance.</em></h1>
        <p class="lead">Warm, welcoming classes for every body and every level. Slow down, stretch out, and leave feeling lighter than when you walked in.</p>
        <div class="hero-cta">
          <a href="#join" class="btn btn-primary">Start your free week</a>
          <a href="#schedule" class="btn btn-ghost">See the schedule</a>
        </div>
        <div class="hero-meta">
          <div><strong>40+</strong>weekly classes</div>
          <div><strong>12</strong>certified teachers</div>
          <div><strong>4.9</strong>average rating</div>
        </div>
      </div>
      <div class="hero-art" role="img" aria-label="Illustration of a person seated in meditation at sunrise">
        <svg viewBox="0 0 400 260" fill="currentColor" aria-hidden="true">
          <circle cx="200" cy="92" r="26"/>
          <path d="M200 124c-34 0-56 22-62 56-30 6-58 22-58 36 0 10 14 18 36 18h168c22 0 36-8 36-18 0-14-28-30-58-36-6-34-28-56-62-56z"/>
        </svg>
      </div>
    </div>
  </section>

  <!-- CLASSES -->
  <section id="classes" class="alt">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Our classes</p>
        <h2>A practice for every mood</h2>
        <p class="lead">Whether you want to sweat, soften or simply rest, there is a class for where you are today.</p>
      </div>
      <div class="cards">
        <article class="card">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M3 12c3-6 6-6 9 0s6 6 9 0"/></svg></div>
          <h3>Vinyasa Flow</h3>
          <p>Breath-led movement that builds strength, heat and focus. Energizing and creative.</p>
          <span class="tag">All levels &middot; 60 min</span>
        </article>
        <article class="card">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/></svg></div>
          <h3>Yin Yoga</h3>
          <p>Long, quiet holds that release deep tension in the hips, back and shoulders.</p>
          <span class="tag">All levels &middot; 75 min</span>
        </article>
        <article class="card">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 3c2 3 4 5 4 8a4 4 0 0 1-8 0c0-3 2-5 4-8z"/><path d="M5 20h14"/></svg></div>
          <h3>Restorative</h3>
          <p>Fully supported poses with bolsters and blankets. Calm your nervous system and recover.</p>
          <span class="tag">Gentle &middot; 60 min</span>
        </article>
        <article class="card">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 4v16M5 11l7-7 7 7"/></svg></div>
          <h3>Yoga Basics</h3>
          <p>New to yoga? Learn the foundations, alignment and breathing in a friendly, no-pressure room.</p>
          <span class="tag">Beginners &middot; 60 min</span>
        </article>
      </div>
    </div>
  </section>

  <!-- SCHEDULE -->
  <section id="schedule">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Weekly schedule</p>
        <h2>Come as you are, any day</h2>
        <p class="lead">A sample of our week. Book a spot in advance, as classes are small by design.</p>
      </div>
      <div class="schedule scroll-x">
        <table>
          <thead>
            <tr><th>Day</th><th>Time</th><th>Class</th><th>Teacher</th></tr>
          </thead>
          <tbody>
            <tr><td>Monday</td><td>7:00 am</td><td>Vinyasa Flow</td><td>Maya</td></tr>
            <tr><td>Monday</td><td>6:30 pm</td><td>Yoga Basics</td><td>Daniel</td></tr>
            <tr><td>Wednesday</td><td>12:15 pm</td><td>Lunchtime Flow <small>(45 min)</small></td><td>Priya</td></tr>
            <tr><td>Wednesday</td><td>7:30 pm</td><td>Yin Yoga</td><td>Maya</td></tr>
            <tr><td>Friday</td><td>6:00 pm</td><td>Restorative</td><td>Elena</td></tr>
            <tr><td>Saturday</td><td>9:00 am</td><td>Vinyasa Flow</td><td>Daniel</td></tr>
            <tr><td>Sunday</td><td>10:00 am</td><td>Yin + Sound Bath</td><td>Priya &amp; Elena</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- ABOUT -->
  <section id="about" class="alt about">
    <div class="wrap about-grid">
      <div class="about-art" role="img" aria-label="Decorative lotus illustration">
        <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <path d="M50 14c9 12 14 22 14 32a14 14 0 0 1-28 0c0-10 5-20 14-32z"/>
          <path d="M50 74c-14 0-28-9-34-26 12 0 22 6 28 14"/>
          <path d="M50 74c14 0 28-9 34-26-12 0-22 6-28 14"/>
          <path d="M24 84c18 6 34 6 52 0"/>
        </svg>
      </div>
      <div>
        <p class="eyebrow">Our story</p>
        <h2>A room that feels like exhale</h2>
        <p style="margin-top:18px">Stillwater began with a simple idea: yoga should feel like coming home, not like a performance. Our light-filled studio is small on purpose, with no mirrors, no pressure and no one watching how deep you go.</p>
        <p>Our teachers are trained, kind and curious. They will help you find a version of every pose that works for your body today.</p>
        <ul class="checks">
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>Small classes (max 14) for real attention</li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>Mats, blocks, bolsters and towels provided</li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>Beginners, seniors and prenatal students welcome</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- PRICING -->
  <section id="pricing">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Membership</p>
        <h2>Simple, honest pricing</h2>
        <p class="lead">No contracts and no hidden fees. Pause or cancel anytime.</p>
      </div>
      <div class="pricing">
        <div class="plan">
          <h3>Drop-in</h3>
          <div class="price">$22 <span>/ class</span></div>
          <p class="note">Perfect for trying us out.</p>
          <ul><li>Any class, any time</li><li>Mat rental included</li><li>Book up to 7 days ahead</li></ul>
          <a href="#join" class="btn btn-ghost">Book a class</a>
        </div>
        <div class="plan featured">
          <span class="badge">Most popular</span>
          <h3>Unlimited</h3>
          <div class="price">$99 <span>/ month</span></div>
          <p class="note">Practice as often as you like.</p>
          <ul><li>Unlimited classes</li><li>Priority booking</li><li>Free guest pass monthly</li><li>10% off workshops</li></ul>
          <a href="#join" class="btn btn-primary">Start free week</a>
        </div>
        <div class="plan">
          <h3>10-Class Pack</h3>
          <div class="price">$180 <span>/ pack</span></div>
          <p class="note">Flexible, valid for 4 months.</p>
          <ul><li>Any class, any time</li><li>Shareable with a friend</li><li>Book up to 7 days ahead</li></ul>
          <a href="#join" class="btn btn-ghost">Buy a pack</a>
        </div>
      </div>
    </div>
  </section>

  <!-- TESTIMONIALS -->
  <section class="alt">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Kind words</p>
        <h2>Our community</h2>
      </div>
      <div class="quotes">
        <figure class="quote">
          <div class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <blockquote>&ldquo;I walked in stressed and stiff, and walked out feeling like a new person. The teachers are wonderful.&rdquo;</blockquote>
          <figcaption>Sarah K., member since 2023</figcaption>
        </figure>
        <figure class="quote">
          <div class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <blockquote>&ldquo;I was nervous about my first class. The Basics course made me feel completely at ease.&rdquo;</blockquote>
          <figcaption>James L., Basics graduate</figcaption>
        </figure>
        <figure class="quote">
          <div class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <blockquote>&ldquo;Yin on Wednesday night is the best part of my week. I sleep better and my back finally stopped hurting.&rdquo;</blockquote>
          <figcaption>Anita R., Unlimited member</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section>
    <div class="wrap">
      <div class="section-head" style="text-align:center">
        <p class="eyebrow">Good to know</p>
        <h2>Questions, answered</h2>
      </div>
      <div class="faq">
        <details>
          <summary>I have never done yoga. Can I join?</summary>
          <p>Absolutely. Our Yoga Basics class is designed for first-timers, and every teacher offers options for all levels.</p>
        </details>
        <details>
          <summary>What should I bring?</summary>
          <p>Just yourself and a water bottle. We provide mats, props and towels. Wear something comfortable that you can move in.</p>
        </details>
        <details>
          <summary>How does the free first week work?</summary>
          <p>Sign up with your name and email and you can attend any class for seven days at no cost. There is no card required and no obligation to continue.</p>
        </details>
        <details>
          <summary>What is your cancellation policy?</summary>
          <p>Cancel a booking up to 3 hours before class for no charge. Memberships can be paused or cancelled anytime.</p>
        </details>
      </div>
    </div>
  </section>

  <!-- JOIN -->
  <section id="join" style="padding-top:0">
    <div class="wrap">
      <div class="cta">
        <div>
          <h2>Your first week is on us</h2>
          <p>Try any class for seven days, free. Tell us a little about you and we will send your welcome guide and booking link.</p>
        </div>
        <div>
          <form id="signup" novalidate>
            <label>Name
              <input type="text" name="name" autocomplete="name" required placeholder="Your name">
            </label>
            <label>Email
              <input type="email" name="email" autocomplete="email" required placeholder="you@example.com">
            </label>
            <label>Experience
              <select name="level">
                <option>Brand new to yoga</option>
                <option>Some experience</option>
                <option>Regular practitioner</option>
              </select>
            </label>
            <button type="submit" class="btn">Claim my free week</button>
            <p class="form-note">We will only email you about your trial. Unsubscribe anytime.</p>
          </form>
          <div id="thanks" role="status" aria-live="polite">
            <strong>Thank you!</strong> Check your inbox for your welcome guide. We can't wait to see you on the mat.
          </div>
        </div>
      </div>
    </div>
  </section>

</main>

<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a href="#top" class="logo" style="margin-bottom:14px">
          <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M16 4c3 4 5 7 5 11a5 5 0 0 1-10 0c0-4 2-7 5-11z"/><path d="M4 22c4 0 8 2 12 6 4-4 8-6 12-6"/></svg>
          Stillwater
        </a>
        <p>A small, friendly yoga studio for every body.</p>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li>123 Garden Lane</li>
          <li>Your City, ST 00000</li>
          <li>Mon&ndash;Fri 6am&ndash;8pm<br>Sat&ndash;Sun 8am&ndash;1pm</li>
        </ul>
      </div>
      <div>
        <h4>Connect</h4>
        <ul>
          <li><a href="mailto:hello@stillwateryoga.example">hello@stillwateryoga.example</a></li>
          <li><a href="tel:+10000000000">(000) 000-0000</a></li>
          <li><a href="#">Instagram</a></li>
        </ul>
      </div>
    </div>
    <p class="copy">&copy; <span id="yr">2026</span> Stillwater Yoga. All rights reserved.</p>
  </div>
</footer>

<script>
  document.getElementById('yr').textContent = new Date().getFullYear();

  const form = document.getElementById('signup');
  const thanks = document.getElementById('thanks');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const name = form.elements.name.value.trim();
    const email = form.elements.email.value.trim();
    if (!name || !/^\S+@\S+\.\S+$/.test(email)) {
      (name ? form.elements.email : form.elements.name).focus();
      return;
    }
    // TODO: send to your email tool or backend (Mailchimp, ConvertKit, Formspree, etc.)
    form.style.display = 'none';
    thanks.style.display = 'block';
  });
</script>
</body>
</html>
```

**What's in it**
- Sticky nav, hero with a clear "free first week" call to action, class types, weekly schedule, about section, pricing, testimonials, FAQ, signup form and footer.
- The page is responsive, supports automatic dark mode, and respects reduced-motion settings. Buttons and the form have visible focus states and proper labels.

**To make it yours**
1. Swap the name, address, contact details, prices, schedule and testimonials. All the sample text is placeholder.
2. Wire up the signup form. It currently just shows a thank-you message. Look for the `TODO` in the script and connect it to Formspree, Mailchimp or your booking tool.
3. Replace the illustrated hero with real studio photos when you have them. Change the `.hero-art` block to an `<img>` and add `object-fit: cover`.
4. Change the colors by editing the variables at the top of the CSS (`--sage`, `--clay`, `--bg`).

Tell me the studio's real name, location, style (hot yoga, prenatal, or something else) and brand colors, and I can tailor the copy and design to match.
