```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Willow Breath Yoga | Book a first class</title>
  <meta name="description" content="A welcoming neighborhood yoga studio for beginners and returning students. See the weekly schedule and book your first class.">
  <script>document.documentElement.className = 'js';</script>
  <style>
    :root {
      /* Palette: three colors plus neutral ink and white */
      --forest: #2F4F44;   /* headings, footer, links */
      --clay: #9C4A2F;     /* primary action, accents */
      --mist: #E8EFEB;     /* soft section background (cool sage tint) */
      --ink: #1F2A26;      /* body text */
      --ink-soft: #4A5753; /* secondary text */
      --line: #C5D1CB;
      --field-border: #6B7A74;
      --serif: Georgia, "Times New Roman", serif;
      --sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --gutter: 16px;
    }

    *, *::before, *::after { box-sizing: border-box; }
    html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }

    body {
      margin: 0;
      font-family: var(--sans);
      font-size: 1.0625rem;
      line-height: 1.6;
      color: var(--ink);
      background: #fff;
    }
    img, svg { display: block; max-width: 100%; }
    h1, h2, h3 {
      font-family: var(--serif);
      font-weight: 700;
      line-height: 1.15;
      color: var(--forest);
      margin: 0 0 0.5em;
    }
    h1 { font-size: 2.25rem; }
    h2 { font-size: 1.875rem; }
    h3 { font-size: 1.25rem; margin-bottom: 0.25em; }
    p { margin: 0 0 1em; }
    a { color: var(--forest); text-underline-offset: 3px; }
    a:hover { color: var(--clay); }

    :focus-visible { outline: 3px solid var(--clay); outline-offset: 3px; }
    .site-footer :focus-visible { outline-color: #fff; }

    .wrap { width: 100%; max-width: 1120px; margin-inline: auto; padding-inline: var(--gutter); }
    .sr-only {
      position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0;
      overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
    }
    .skip-link {
      position: absolute; left: var(--gutter); top: -100px; z-index: 20;
      background: #fff; color: var(--forest); padding: 10px 14px; border: 2px solid var(--forest);
    }
    .skip-link:focus { top: 8px; }

    /* Buttons: modest radius, not pills */
    .btn {
      display: inline-block;
      min-height: 48px;
      padding: 12px 22px;
      border: 2px solid var(--clay);
      border-radius: 6px;
      background: var(--clay);
      color: #fff;
      font: 600 1rem/1.4 var(--sans);
      text-decoration: none;
      text-align: center;
      cursor: pointer;
    }
    .btn:hover { background: #7F3A24; border-color: #7F3A24; color: #fff; }
    .btn-sm { min-height: 44px; padding: 8px 16px; }
    .btn-outline { background: transparent; color: var(--clay); }
    .btn-outline:hover { background: var(--clay); color: #fff; }

    /* Header */
    .site-header {
      position: sticky; top: 0; z-index: 10;
      background: #fff;
      border-bottom: 1px solid var(--line);
    }
    .bar { display: flex; align-items: center; gap: 8px; min-height: 64px; }
    .brand {
      margin-right: auto;
      font: 700 1.125rem/1.2 var(--serif);
      color: var(--forest);
      text-decoration: none;
      min-width: 0;
    }
    .brand:hover { color: var(--forest); }
    .menu-toggle {
      display: none;
      min-height: 44px; padding: 8px 14px;
      border: 2px solid var(--forest); border-radius: 6px;
      background: #fff; color: var(--forest);
      font: 600 1rem/1.2 var(--sans);
      cursor: pointer;
    }
    .js .menu-toggle { display: block; }
    .site-nav {
      position: absolute; top: 100%; left: 0; right: 0;
      background: #fff; border-bottom: 1px solid var(--line);
    }
    .js .site-nav { display: none; }
    .js .site-nav.open { display: block; }
    .site-nav ul { list-style: none; margin: 0; padding: 8px var(--gutter) 16px; }
    .site-nav a {
      display: block; padding: 12px 0;
      color: var(--ink); text-decoration: none; font-weight: 600;
      border-bottom: 1px solid var(--line);
    }
    .site-nav li:last-child a { border-bottom: 0; }
    .site-nav a:hover { color: var(--clay); }

    /* Sections */
    section { padding-block: 56px; scroll-margin-top: 72px; }
    .tint { background: var(--mist); }
    .lead { font-size: 1.125rem; color: var(--ink-soft); max-width: 40rem; }

    /* Hero */
    .hero { padding-block: 40px 56px; background: var(--mist); }
    .hero h1 { max-width: 14ch; }
    .hero .lead { margin-bottom: 1.5rem; }
    .hero-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 24px; }

    /* About */
    .about p { max-width: 42rem; }

    /* Schedule */
    .schedule { list-style: none; margin: 24px 0 0; padding: 0; border-top: 1px solid var(--line); }
    .class {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 4px 16px;
      align-items: center;
      padding: 16px 0;
      border-bottom: 1px solid var(--line);
    }
    .class .when { grid-column: 1 / -1; margin: 0; font-weight: 700; color: var(--clay); }
    .class .when span { color: var(--ink); font-weight: 600; margin-left: 8px; }
    .class h3 { margin: 0; }
    .class .meta { margin: 0; color: var(--ink-soft); font-size: 0.9375rem; }
    .class .book-link { font-weight: 600; white-space: nowrap; }

    /* Cards */
    .grid { display: grid; gap: 24px; margin-top: 24px; }
    .photo { width: 100%; aspect-ratio: 4 / 3; border-radius: 6px; margin-bottom: 16px; }
    .role { margin: 0 0 8px; font-weight: 600; color: var(--clay); }
    .teacher p:last-child { margin-bottom: 0; }

    .tier {
      background: #fff;
      border: 1px solid var(--line);
      border-top: 4px solid var(--forest);
      border-radius: 6px;
      padding: 24px 20px;
      display: flex; flex-direction: column;
    }
    .tier.featured { border-top-color: var(--clay); }
    .tier .flag { margin: 0 0 4px; font-size: 0.875rem; font-weight: 700; color: var(--clay); }
    .tier .price { font: 700 2.25rem/1.1 var(--serif); color: var(--forest); margin: 8px 0 4px; }
    .tier .price span { font: 400 1rem/1.4 var(--sans); color: var(--ink-soft); }
    .tier ul { margin: 16px 0 24px; padding-left: 1.2em; color: var(--ink); }
    .tier li { margin-bottom: 6px; }
    .tier .btn { margin-top: auto; }

    /* Testimonials */
    blockquote { margin: 0; padding: 0 0 0 20px; border-left: 4px solid var(--clay); }
    blockquote p { font: 1.25rem/1.5 var(--serif); color: var(--forest); margin-bottom: 8px; }
    blockquote footer { color: var(--ink-soft); font-size: 0.9375rem; }

    /* Visit */
    address { font-style: normal; margin-bottom: 1em; }
    .hours { display: grid; grid-template-columns: auto 1fr; gap: 6px 20px; margin: 0; }
    .hours dt { font-weight: 600; }
    .hours dd { margin: 0; }
    .map { width: 100%; aspect-ratio: 4 / 3; border-radius: 6px; border: 1px solid var(--line); background: #fff; }

    /* Booking form */
    .book-form {
      max-width: 560px; margin-top: 24px; padding: 20px;
      border: 1px solid var(--line); border-radius: 6px; background: #fff;
    }
    .field { margin-bottom: 18px; }
    .field label { display: block; margin-bottom: 6px; font-weight: 600; color: var(--ink); }
    .field input, .field select {
      width: 100%; min-height: 48px; padding: 10px 12px;
      font: 1rem/1.4 var(--sans); color: var(--ink);
      background: #fff; border: 1px solid var(--field-border); border-radius: 6px;
    }
    .field input:focus-visible, .field select:focus-visible { outline: 3px solid var(--clay); outline-offset: 1px; }
    .book-form .btn { width: 100%; }

    /* Footer */
    .site-footer { background: var(--forest); color: #fff; padding-block: 40px; }
    .site-footer a { color: #fff; }
    .site-footer a:hover { color: #fff; text-decoration-thickness: 2px; }
    .site-footer .name { font: 700 1.25rem/1.2 var(--serif); margin: 0 0 12px; }
    .social { list-style: none; margin: 0 0 20px; padding: 0; display: flex; gap: 24px; }
    .social a { display: inline-block; padding: 8px 0; }
    .copy { margin: 0; font-size: 0.9375rem; }

    /* Tablet and up */
    @media (min-width: 720px) {
      :root { --gutter: 24px; }
      h1 { font-size: 3rem; }
      h2 { font-size: 2.25rem; }
      section { padding-block: 80px; }
      .hero { padding-block: 72px 88px; }
      .grid.three { grid-template-columns: repeat(3, 1fr); }
      .grid.two { grid-template-columns: 1fr 1fr; align-items: start; gap: 48px; }
      .class { grid-template-columns: 220px 1fr auto; gap: 16px 24px; padding: 20px 0; }
      .class .when { grid-column: auto; }
      .quotes { grid-template-columns: 1fr 1fr; gap: 48px; }
      .book-form { padding: 32px; }
    }

    /* Desktop nav */
    @media (min-width: 880px) {
      .menu-toggle, .js .menu-toggle { display: none; }
      .site-nav, .js .site-nav { display: block; position: static; background: none; border: 0; margin-left: auto; }
      .site-nav ul { display: flex; gap: 24px; padding: 0; }
      .site-nav a { padding: 8px 0; border: 0; }
      .brand { margin-right: 0; }
      .bar { gap: 32px; }
    }
    @media (min-width: 1100px) {
      h1 { font-size: 3.5rem; }
      :root { --gutter: 32px; }
    }
  </style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header" id="top">
    <div class="wrap bar">
      <a class="brand" href="#top">Willow Breath Yoga</a>
      <nav id="site-nav" class="site-nav" aria-label="Primary">
        <ul>
          <li><a href="#about">About</a></li>
          <li><a href="#schedule">Schedule</a></li>
          <li><a href="#teachers">Teachers</a></li>
          <li><a href="#membership">Membership</a></li>
          <li><a href="#visit">Visit</a></li>
        </ul>
      </nav>
      <a class="btn btn-sm" href="#book">Book</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    </div>
  </header>

  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap">
        <h1 id="hero-title">Find your calm. Build your strength.</h1>
        <p class="lead">A neighborhood studio where calm, strength, and community grow with every class.</p>
        <div class="hero-actions">
          <a class="btn" href="#book">Book a first class</a>
          <a href="#schedule">See the weekly schedule</a>
        </div>
      </div>
    </section>

    <section id="about" class="about" aria-labelledby="about-title">
      <div class="wrap">
        <h2 id="about-title">Yoga that meets you where you are</h2>
        <p class="lead">Willow Breath is a small, friendly studio for people at every stage of practice. If you have never stepped onto a mat, our teachers explain each pose in plain language and offer simple options so nothing feels out of reach.</p>
        <p>If you are returning after a break, or you practice already and want a steadier routine, you will find slower classes to rebuild gently and stronger flows to keep you challenged. Classes are capped at 18 students so every person gets attention. Mats, blocks, and blankets are provided, and you can arrive five minutes early to say hello and settle in.</p>
      </div>
    </section>

    <section id="schedule" class="tint" aria-labelledby="schedule-title">
      <div class="wrap">
        <h2 id="schedule-title">Class schedule</h2>
        <p class="lead">A sample week. New to yoga? Start with Gentle Hatha or Foundations.</p>
        <ul class="schedule">
          <li class="class">
            <p class="when">Monday <span>6:30 pm</span></p>
            <div>
              <h3>Vinyasa Flow</h3>
              <p class="meta">Level: All levels &middot; Teacher: Maya</p>
            </div>
            <a class="book-link" href="#book">Book<span class="sr-only"> Vinyasa Flow on Monday</span></a>
          </li>
          <li class="class">
            <p class="when">Tuesday <span>9:00 am</span></p>
            <div>
              <h3>Gentle Hatha</h3>
              <p class="meta">Level: Beginner &middot; Teacher: Daniel</p>
            </div>
            <a class="book-link" href="#book">Book<span class="sr-only"> Gentle Hatha on Tuesday</span></a>
          </li>
          <li class="class">
            <p class="when">Wednesday <span>7:00 pm</span></p>
            <div>
              <h3>Yin</h3>
              <p class="meta">Level: All levels &middot; Teacher: Priya</p>
            </div>
            <a class="book-link" href="#book">Book<span class="sr-only"> Yin on Wednesday</span></a>
          </li>
          <li class="class">
            <p class="when">Thursday <span>6:30 pm</span></p>
            <div>
              <h3>Restorative</h3>
              <p class="meta">Level: All levels &middot; Teacher: Priya</p>
            </div>
            <a class="book-link" href="#book">Book<span class="sr-only"> Restorative on Thursday</span></a>
          </li>
          <li class="class">
            <p class="when">Saturday <span>9:30 am</span></p>
            <div>
              <h3>Foundations</h3>
              <p class="meta">Level: Beginner &middot; Teacher: Daniel</p>
            </div>
            <a class="book-link" href="#book">Book<span class="sr-only"> Foundations on Saturday</span></a>
          </li>
          <li class="class">
            <p class="when">Sunday <span>10:00 am</span></p>
            <div>
              <h3>Slow Flow</h3>
              <p class="meta">Level: Intermediate &middot; Teacher: Maya</p>
            </div>
            <a class="book-link" href="#book">Book<span class="sr-only"> Slow Flow on Sunday</span></a>
          </li>
        </ul>
      </div>
    </section>

    <section id="teachers" aria-labelledby="teachers-title">
      <div class="wrap">
        <h2 id="teachers-title">Meet your teachers</h2>
        <div class="grid three">
          <article class="teacher">
            <svg class="photo" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Placeholder portrait of Maya">
              <rect width="400" height="300" fill="#E8EFEB"/>
              <circle cx="200" cy="120" r="52" fill="#2F4F44" opacity=".35"/>
              <path d="M90 300c0-70 50-110 110-110s110 40 110 110z" fill="#2F4F44" opacity=".35"/>
            </svg>
            <h3>Maya</h3>
            <p class="role">Vinyasa and Slow Flow</p>
            <p>Maya has taught for nine years and loves helping people link breath to movement. Her classes are steady, musical, and full of clear cues.</p>
          </article>
          <article class="teacher">
            <svg class="photo" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Placeholder portrait of Daniel">
              <rect width="400" height="300" fill="#E8EFEB"/>
              <circle cx="200" cy="120" r="52" fill="#2F4F44" opacity=".35"/>
              <path d="M90 300c0-70 50-110 110-110s110 40 110 110z" fill="#2F4F44" opacity=".35"/>
            </svg>
            <h3>Daniel</h3>
            <p class="role">Gentle Hatha and Foundations</p>
            <p>Daniel came to yoga to ease a stiff back and stayed to teach. He breaks poses down patiently and is the first person to say "take the easier version."</p>
          </article>
          <article class="teacher">
            <svg class="photo" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Placeholder portrait of Priya">
              <rect width="400" height="300" fill="#E8EFEB"/>
              <circle cx="200" cy="120" r="52" fill="#2F4F44" opacity=".35"/>
              <path d="M90 300c0-70 50-110 110-110s110 40 110 110z" fill="#2F4F44" opacity=".35"/>
            </svg>
            <h3>Priya</h3>
            <p class="role">Yin and Restorative</p>
            <p>Priya teaches slow, supported classes for rest and recovery. After a long day, her room is quiet, warm, and unhurried.</p>
          </article>
        </div>
      </div>
    </section>

    <section id="membership" class="tint" aria-labelledby="membership-title">
      <div class="wrap">
        <h2 id="membership-title">Membership</h2>
        <p class="lead">Simple options, with no joining fee. Pick what fits how often you want to practice.</p>
        <div class="grid three">
          <article class="tier">
            <h3>Drop-in</h3>
            <p class="price">$20 <span>per class</span></p>
            <ul>
              <li>One class, any style</li>
              <li>Book up to 7 days ahead</li>
              <li>Mat rental $2</li>
            </ul>
            <a class="btn btn-outline" href="#book">Book a drop-in</a>
          </article>
          <article class="tier featured">
            <p class="flag">Most popular</p>
            <h3>10-class pack</h3>
            <p class="price">$170 <span>($17 per class)</span></p>
            <ul>
              <li>Use on any class</li>
              <li>Valid for 5 months</li>
              <li>Share with a friend</li>
            </ul>
            <a class="btn" href="#book">Book with a pack</a>
          </article>
          <article class="tier">
            <h3>Unlimited monthly</h3>
            <p class="price">$99 <span>per month</span></p>
            <ul>
              <li>Every class on the schedule</li>
              <li>Free mat rental</li>
              <li>Pause once a year</li>
            </ul>
            <a class="btn btn-outline" href="#book">Book with unlimited</a>
          </article>
        </div>
      </div>
    </section>

    <section id="testimonials" aria-labelledby="testimonials-title">
      <div class="wrap">
        <h2 id="testimonials-title">What students say</h2>
        <!-- PLACEHOLDER: these two quotes are sample text. Replace with real, permissioned student testimonials before launch. -->
        <div class="grid quotes">
          <blockquote>
            <p>I was nervous about my first class, but nobody rushed me. By the end I was smiling and my shoulders were finally down from my ears.</p>
            <footer>Beginner student</footer>
          </blockquote>
          <blockquote>
            <p>I came back to yoga after years away. The slower classes helped me rebuild, and now Sunday Slow Flow is my favorite hour of the week.</p>
            <footer>Returning student</footer>
          </blockquote>
        </div>
      </div>
    </section>

    <section id="visit" class="tint" aria-labelledby="visit-title">
      <div class="wrap">
        <h2 id="visit-title">Visit the studio</h2>
        <div class="grid two">
          <div>
            <address>123 Example Street, Your City</address>
            <p>Look for the green door. Street parking is nearby, and the studio is a short walk from public transit.</p>
            <h3>Opening hours</h3>
            <dl class="hours">
              <dt>Monday to Friday</dt><dd>6:00 am to 8:30 pm</dd>
              <dt>Saturday</dt><dd>8:00 am to 1:00 pm</dd>
              <dt>Sunday</dt><dd>9:00 am to 1:00 pm</dd>
            </dl>
          </div>
          <svg class="map" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Map placeholder showing the studio location">
            <rect width="400" height="300" fill="#E8EFEB"/>
            <path d="M0 210L400 120M120 0L180 300M260 0L300 300" stroke="#C5D1CB" stroke-width="14" fill="none"/>
            <path d="M200 90c-22 0-38 17-38 38 0 28 38 62 38 62s38-34 38-62c0-21-16-38-38-38z" fill="#9C4A2F"/>
            <circle cx="200" cy="128" r="13" fill="#fff"/>
          </svg>
        </div>
      </div>
    </section>

    <section id="book" aria-labelledby="book-title">
      <div class="wrap">
        <h2 id="book-title">Book your first class</h2>
        <p class="lead">Tell us a little about yourself and we will confirm your spot by email.</p>
        <form class="book-form" action="https://example.com/book-a-class" method="post">
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
            <select id="class" name="class" required>
              <option value="">Choose a class</option>
              <option>Vinyasa Flow, Monday 6:30 pm</option>
              <option>Gentle Hatha, Tuesday 9:00 am</option>
              <option>Yin, Wednesday 7:00 pm</option>
              <option>Restorative, Thursday 6:30 pm</option>
              <option>Foundations, Saturday 9:30 am</option>
              <option>Slow Flow, Sunday 10:00 am</option>
              <option>Not sure yet, help me choose</option>
            </select>
          </div>
          <button class="btn" type="submit">Book my first class</button>
        </form>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <p class="name">Willow Breath Yoga</p>
      <ul class="social">
        <li><a href="https://www.instagram.com/example">Instagram</a></li>
        <li><a href="https://www.facebook.com/example">Facebook</a></li>
      </ul>
      <p class="copy">&copy; 2026 Willow Breath Yoga. All rights reserved.</p>
    </div>
  </footer>

  <script>
    var toggle = document.querySelector('.menu-toggle');
    var nav = document.getElementById('site-nav');
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  </script>
</body>
</html>
```

Built a single-file `index.html` landing page for a sample studio, "Willow Breath Yoga": nine sections in the order you gave, a sticky header with an always-visible Book button, a three-color palette (forest, clay, mist) as `:root` custom properties, system Georgia and system sans fonts, and a mobile-first layout with a 16px gutter.
Verified by reading the CSS only. I had no headless browser here, so I did not render it at 375px or 1440px. By inspection, the header, hero, schedule list, cards and form are fluid with `max-width: 100%` media, so I expect no horizontal scroll. The hero button should sit well above the fold at 375px. I computed contrast by hand (body text, white on clay and clay on mist are all above 4.5:1), but none of it has been checked in a real browser or with an automated audit.
Still placeholders: studio name, teachers and bios, prices, hours, the "123 Example Street, Your City" address, the SVG portraits and map, the two testimonials (marked in an HTML comment), the Instagram and Facebook links, and the form action `https://example.com/book-a-class`.
