#!/usr/bin/env python3
"""P070 Sauna club website template: one static page, no dependencies, no outside requests.

Writes templates/sauna-club-website/: index.html, styles.css, assets/*.svg, fonts/*.woff2 + OFL.txt.
LICENSE, README.md and LISTING.md are written by w3s_listings.py; preview.png by w3s_check70.js + this file (--preview).
"""
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w3s_common as S  # noqa: E402

SLUG = "sauna-club-website"
OUT = os.path.join(S.ROOT, SLUG)

CSS = r"""/* Sauna club website template. Code: MIT License, (c) 2026 DIVELUX (https://diveluxsaunahat.com).
   Change the look in :root below: colors, fonts, widths. Everything else reads these variables. */

@font-face{font-family:"Bricolage Grotesque";src:url(fonts/bricolage-grotesque-latin.woff2) format("woff2");
  font-weight:200 800;font-stretch:75% 100%;font-display:swap}
@font-face{font-family:"Inter";src:url(fonts/inter-latin.woff2) format("woff2");font-weight:100 900;font-display:swap}

:root{
  --paper:#f6f3ee; --paper-2:#efe9df; --card:#fffdf9; --ink:#1b1512; --ink-2:#3d332c; --muted:#6f655c;
  --line:#ded6ca; --night:#1c110b; --night-2:#2a1b13; --on-night:#f6f3ee; --on-night-2:#d9cbbb;
  --accent:#f0762e;            /* one accent: the main button and small markers only */
  --on-accent:#1b1512;
  --display:"Bricolage Grotesque","Arial Narrow",Arial,sans-serif;
  --body:"Inter",system-ui,-apple-system,"Segoe UI",Arial,sans-serif;
  --wide:1160px; --gutter:20px; --r:6px;
  --s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:32px;--s7:48px;--s8:64px;--s9:96px;
  --fast:150ms;
}

*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.6 var(--body)}
img,svg{display:block;max-width:100%;height:auto}
h1,h2,h3{font-family:var(--display);font-weight:700;line-height:1.05;letter-spacing:-.015em;margin:0;text-wrap:balance}
p,ul,ol,dl,figure{margin:0}
a{color:inherit;text-underline-offset:.18em}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px;border-radius:2px}
.on-night :focus-visible,.on-night:focus-visible{outline-color:var(--on-night)}

.skip{position:absolute;left:var(--s4);top:-100px;z-index:10;background:var(--ink);color:var(--paper);padding:var(--s3) var(--s4);
  border-radius:var(--r);text-decoration:none;font-weight:600}
.skip:focus{top:var(--s4)}
.wrap{width:100%;max-width:calc(var(--wide) + 2 * var(--gutter));margin:0 auto;padding:0 var(--gutter)}

/* header + nav: on phones the links scroll sideways, no menu script needed */
.site-head{border-bottom:1px solid var(--line);background:var(--paper)}
.site-head .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s2) var(--s5);padding-top:var(--s3);padding-bottom:var(--s3)}
.brand{display:flex;align-items:center;gap:var(--s3);text-decoration:none;font-family:var(--display);font-weight:700;font-size:20px;
  min-height:44px;margin-right:auto}
.brand img{width:36px;height:36px}
.nav{order:3;flex:1 0 100%;overflow-x:auto;scrollbar-width:none;margin:0 calc(-1 * var(--gutter));padding:0 var(--gutter)}
.nav::-webkit-scrollbar{display:none}
.nav{-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}
.sm-hide{display:none}
.nav ul{display:flex;gap:var(--s1);list-style:none;padding:0;margin:0}
.nav a{display:flex;align-items:center;min-height:44px;padding:0 var(--s3);text-decoration:none;font-weight:500;white-space:nowrap;border-radius:var(--r)}
.nav a:hover{background:var(--paper-2)}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 var(--s5);border-radius:var(--r);
  font:600 16px/1.2 var(--body);text-decoration:none;border:2px solid transparent;transition:background-color var(--fast),transform var(--fast)}
.btn-main{background:var(--accent);color:var(--on-accent)}
.btn-main:hover{background:#e8661b}
.btn-main:active{transform:translateY(1px)}
.btn-small{min-height:44px;padding:0 var(--s4);font-size:15px}
.quiet{font-weight:600;min-height:44px;display:inline-flex;align-items:center}

/* hero */
.hero{padding:var(--s7) 0 var(--s8)}
.hero .wrap{display:grid;gap:var(--s6);align-items:center}
.kicker{font-weight:600;color:var(--ink-2);margin-bottom:var(--s3)}
.hero h1{font-size:clamp(40px,9vw,76px);max-width:14ch}
.lead{font-size:clamp(18px,2.2vw,21px);line-height:1.5;color:var(--ink-2);margin-top:var(--s4);max-width:36ch}
.actions{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s3) var(--s5);margin-top:var(--s5)}
.hero figure img{width:min(100%,300px);margin:0 auto}
.facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--s4);margin-top:var(--s6);padding-top:var(--s4);border-top:2px solid var(--ink);max-width:560px}
.facts dt{font-size:14px;color:var(--muted)}
.facts dd{margin:0;font-family:var(--display);font-weight:700;font-size:clamp(18px,2.4vw,22px);line-height:1.2}

/* sections */
.sec{padding:var(--s8) 0}
.sec-head{display:grid;gap:var(--s3);margin-bottom:var(--s6);max-width:680px}
.sec-head h2{font-size:clamp(32px,5.5vw,52px)}
.sec-head p{color:var(--ink-2)}
.band{background:var(--paper-2)}

/* schedule table: scrolls sideways inside its box on small screens */
.table-box{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--card)}
table{width:100%;min-width:720px;border-collapse:collapse;font-variant-numeric:tabular-nums}
caption{text-align:left;padding:var(--s4) var(--s4) var(--s2);font-weight:600;color:var(--ink-2)}
th,td{text-align:left;padding:var(--s3) var(--s4);border-top:1px solid var(--line);vertical-align:top}
thead th{font-size:14px;color:var(--muted);font-weight:600;border-top:2px solid var(--ink)}
tbody th{font-weight:600;white-space:nowrap}
.tag{display:inline-block;font-size:13px;font-weight:600;line-height:1;padding:5px 8px;border:1px solid var(--ink-2);border-radius:999px;margin-left:var(--s1);white-space:nowrap}
.closed{color:var(--muted)}
.nw{white-space:nowrap}
.note{font-size:15px;color:var(--muted);margin-top:var(--s4)}

/* prices */
.prices{display:grid;gap:var(--s4);list-style:none;padding:0}
.price{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:var(--s5);display:flex;flex-direction:column;gap:var(--s2)}
.price h3{font-size:22px}
.price .amount{font-family:var(--display);font-weight:700;font-size:44px;line-height:1;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.price .amount small{font:500 16px var(--body);color:var(--muted);letter-spacing:0}
.price ul{list-style:none;padding:0;margin-top:var(--s2);display:grid;gap:var(--s2);color:var(--ink-2)}
.price li{padding-left:22px;position:relative}
.price li::before{content:"";position:absolute;left:2px;top:.62em;width:8px;height:8px;border-radius:50%;background:var(--ink-2)}
.price.featured{border:2px solid var(--ink)}
.price .badge{align-self:flex-start;font-size:13px;font-weight:600;background:var(--ink);color:var(--paper);padding:4px 10px;border-radius:999px}

/* rules: the dark band */
.night{background:var(--night);color:var(--on-night)}
.night .sec-head p{color:var(--on-night-2)}
.rules{display:grid;gap:0 var(--s6);list-style:none;padding:0;counter-reset:r}
.rules li{counter-increment:r;display:grid;grid-template-columns:48px 1fr;gap:var(--s3);padding:var(--s4) 0;border-top:1px solid #4a3426}
.rules li::before{content:counter(r,decimal-leading-zero);font-family:var(--display);font-weight:700;font-size:20px;color:var(--on-night-2)}
.rules b{display:block;font-weight:600}
.rules span{color:var(--on-night-2)}
.safety{margin-top:var(--s6);padding:var(--s4);border-left:3px solid var(--accent);background:var(--night-2);color:var(--on-night-2);font-size:15px;max-width:760px}

/* visit */
.visit{display:grid;gap:var(--s6)}
.visit dl{display:grid;gap:var(--s4)}
.visit dt{font-size:14px;color:var(--muted);font-weight:600}
.visit dd{margin:0;font-size:18px}
.visit address{font-style:normal}
.hours{list-style:none;padding:0;display:grid;gap:2px}
.hours li{display:flex;justify-content:space-between;gap:var(--s4);max-width:320px;font-variant-numeric:tabular-nums}
.map{min-height:280px;border:2px dashed var(--muted);border-radius:var(--r);display:grid;place-content:center;gap:var(--s3);
  text-align:center;padding:var(--s5);background:var(--card);color:var(--ink-2)}
.map strong{font-family:var(--display);font-size:24px;color:var(--ink)}

/* FAQ */
.faq{display:grid;gap:0;max-width:760px}
.faq details{border-top:1px solid var(--line)}
.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:var(--s4);min-height:56px;
  padding:var(--s3) 0;font-weight:600;font-size:18px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font:400 28px/1 var(--body);color:var(--ink-2);transition:transform var(--fast)}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{padding:0 0 var(--s4);color:var(--ink-2);max-width:65ch}

/* footer */
.site-foot{background:var(--night-2);color:var(--on-night-2);padding:var(--s7) 0 var(--s6);font-size:15px}
.site-foot .wrap{display:grid;gap:var(--s5)}
.site-foot strong{color:var(--on-night);font-family:var(--display);font-size:20px}
.site-foot a{color:var(--on-night)}
.credit{border-top:1px solid #4a3426;padding-top:var(--s4)}

@media (min-width:480px){.sm-hide{display:inline}}
@media (min-width:640px){
  .scroll-hint{display:none}
  .prices{grid-template-columns:repeat(3,minmax(0,1fr))}
  .rules{grid-template-columns:1fr 1fr}
}
@media (min-width:900px){
  .nav{order:0;flex:0 1 auto;margin:0;padding:0;overflow:visible;-webkit-mask-image:none;mask-image:none}
  .hero figure img{width:min(100%,520px)}
  .hero{padding:var(--s9) 0}
  .hero .wrap{grid-template-columns:1.15fr .85fr;gap:var(--s7)}
  .visit{grid-template-columns:1fr 1.2fr}
  .site-foot .wrap{grid-template-columns:1fr auto}
  .credit{grid-column:1 / -1}
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{transition:none!important;animation:none!important}
}
@media print{
  .site-head .nav,.skip,.actions,.map{display:none}
  .night,.site-foot{background:none;color:#000}
  body{background:#fff}
}
"""

HTML = """<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Your Sauna Club — wood-fired sauna and cold plunge in Your Town</title>
<meta name="description" content="A small public sauna in Your Town: 90-minute sessions, a cold plunge and Aufguss evenings. See the schedule, prices and house rules, and book a session.">
<meta name="theme-color" content="#f6f3ee">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="styles.css">
<!--
  Sauna club website template by DIVELUX (https://diveluxsaunahat.com). Code: MIT License.
  Replace every sample name, address, time and price below with your own. See README.md.
-->
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-head">
  <div class="wrap">
    <a class="brand" href="#top" aria-label="Your Sauna Club, home"><img src="assets/mark.svg" width="36" height="36" alt="">Your Sauna Club</a>
    <nav class="nav" aria-label="Main">
      <ul>
        <li><a href="#schedule">Schedule</a></li>
        <li><a href="#prices">Prices</a></li>
        <li><a href="#rules">House rules</a></li>
        <li><a href="#visit">Visit</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </nav>
    <a class="btn btn-main btn-small" href="#visit">Book<span class="sm-hide">&nbsp;a session</span></a>
  </div>
</header>

<main id="main" tabindex="-1">
  <section class="hero" id="top" aria-labelledby="hero-title">
    <div class="wrap">
      <div>
        <p class="kicker">Wood-fired sauna · cold plunge · Your Town</p>
        <h1 id="hero-title">Heat, steam and a cold plunge, ten minutes from town.</h1>
        <p class="lead">A small public sauna for everyone. Book a 90-minute session, bring two towels and leave the week at the door.</p>
        <div class="actions">
          <a class="btn btn-main" href="#visit">Book a session</a>
          <a class="quiet" href="#schedule">See this week’s schedule</a>
        </div>
        <dl class="facts">
          <div><dt>Session</dt><dd>90 min</dd></div>
          <div><dt>Group size</dt><dd>Up to 12</dd></div>
          <div><dt>Open</dt><dd>Tue–Sun</dd></div>
        </dl>
      </div>
      <figure>
        <img src="assets/lakeside-sauna.svg" width="600" height="600" alt="Drawing of a small wooden sauna cabin by a lake, with smoke rising from the chimney">
      </figure>
    </div>
  </section>

  <section class="sec band" id="schedule" aria-labelledby="schedule-title">
    <div class="wrap">
      <div class="sec-head">
        <h2 id="schedule-title">This week’s sessions</h2>
        <p>Every session is 90 minutes: sauna, cold plunge and time to rest. Aufguss rounds are led by our sauna master.</p>
      </div>
      <div class="table-box" role="region" aria-labelledby="schedule-caption" tabindex="0">
        <table>
          <caption id="schedule-caption">Session start times, week of December 8</caption>
          <thead><tr><th scope="col">Day</th><th scope="col">Morning</th><th scope="col">Afternoon</th><th scope="col">Evening</th></tr></thead>
          <tbody>
            <tr><th scope="row">Monday</th><td class="closed" colspan="3">Closed for cleaning</td></tr>
            <tr><th scope="row">Tuesday</th><td class="closed">—</td><td>4:00 pm</td><td>5:30 pm, 7:00 pm</td></tr>
            <tr><th scope="row">Wednesday</th><td class="closed">—</td><td>4:00 pm</td><td>5:30 pm, 7:00 pm <span class="tag">Aufguss</span></td></tr>
            <tr><th scope="row">Thursday</th><td>7:00 am</td><td>4:00 pm</td><td>5:30 pm, 7:00 pm</td></tr>
            <tr><th scope="row">Friday</th><td class="closed">—</td><td>4:00 pm</td><td>5:30 pm, <span class="nw">7:00 pm <span class="tag">Aufguss</span>,</span> 8:30 pm</td></tr>
            <tr><th scope="row">Saturday</th><td>9:00 am, 10:30 am</td><td>12:00 pm, 1:30 pm, 3:00 pm</td><td>4:30 pm, 6:00 pm, 7:30 pm</td></tr>
            <tr><th scope="row">Sunday</th><td><span class="nw">9:00 am <span class="tag">Women only</span>,</span> 10:30 am</td><td>12:00 pm, 1:30 pm, 3:00 pm</td><td class="closed">—</td></tr>
          </tbody>
        </table>
      </div>
      <p class="note scroll-hint">Swipe the table sideways to see the whole week.</p>
      <p class="note">Times change on holidays. Check this page or call us before you come.</p>
    </div>
  </section>

  <section class="sec" id="prices" aria-labelledby="prices-title">
    <div class="wrap">
      <div class="sec-head">
        <h2 id="prices-title">Prices</h2>
        <p>Tea is included in every session. Towels to rent at the front desk.</p>
      </div>
      <ul class="prices">
        <li class="price">
          <h3>Single session</h3>
          <p class="amount">$25 <small>per person</small></p>
          <ul><li>90 minutes</li><li>Sauna, cold plunge and tea</li><li>Book online or call</li></ul>
        </li>
        <li class="price featured">
          <span class="badge">Best for regulars</span>
          <h3>10-session pass</h3>
          <p class="amount">$200 <small>per pass</small></p>
          <ul><li>Ten sessions, any day</li><li>Share it with a friend</li><li>Valid for 12 months</li></ul>
        </li>
        <li class="price">
          <h3>Monthly membership</h3>
          <p class="amount">$89 <small>per month</small></p>
          <ul><li>Up to 3 sessions a week</li><li>Book 7 days ahead</li><li>Members’ evenings</li></ul>
        </li>
      </ul>
    </div>
  </section>

  <section class="sec night on-night" id="rules" aria-labelledby="rules-title">
    <div class="wrap">
      <div class="sec-head">
        <h2 id="rules-title">House rules</h2>
        <p>A few simple rules keep the sauna clean, calm and friendly for everyone.</p>
      </div>
      <ol class="rules">
        <li><p><b>Shower before the sauna.</b><span>And again after the cold plunge, if you like.</span></p></li>
        <li><p><b>Sit on a towel.</b><span>Every time, on every bench.</span></p></li>
        <li><p><b>Ask before you pour.</b><span>Water on the stones means more steam for everyone in the room.</span></p></li>
        <li><p><b>Keep voices low.</b><span>Phones stay in the lockers.</span></p></li>
        <li><p><b>Swimsuit or towel wrap.</b><span>Please follow the sign for your session.</span></p></li>
        <li><p><b>No alcohol.</b><span>Not before your session and not during it.</span></p></li>
        <li><p><b>Children with an adult.</b><span>Guests under 16 come with a parent or guardian.</span></p></li>
        <li><p><b>Listen to your body.</b><span>Leave the heat right away if you feel dizzy or unwell.</span></p></li>
      </ol>
      <p class="safety">General guidance, not medical advice. If you are pregnant or have a heart condition or other health concern, talk to your doctor before using a sauna or a cold plunge.</p>
    </div>
  </section>

  <section class="sec" id="visit" aria-labelledby="visit-title">
    <div class="wrap">
      <div class="sec-head">
        <h2 id="visit-title">Visit and book</h2>
        <p>Call or email to book a session. Arrive 15 minutes early on your first visit and we will show you around.</p>
      </div>
      <div class="visit">
        <dl>
          <div><dt>Address</dt><dd><address>123 Example Road<br>Your Town, ST 00000</address></dd></div>
          <div><dt>Phone</dt><dd><a href="tel:+15550100123">(555) 010-0123</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:hello@example.com">hello@example.com</a></dd></div>
          <div><dt>Front desk hours</dt><dd>
            <ul class="hours">
              <li><span>Tue–Fri</span><span>3:30–10:00 pm</span></li>
              <li><span>Sat</span><span>8:30 am–9:00 pm</span></li>
              <li><span>Sun</span><span>8:30 am–4:30 pm</span></li>
              <li><span>Mon</span><span>Closed</span></li>
            </ul></dd></div>
        </dl>
        <div class="map" role="region" aria-label="Map">
          <strong>Map goes here</strong>
          <p>Add a map image or a link to your favorite map service.</p>
          <p><a href="https://www.openstreetmap.org/">Open the map</a></p>
        </div>
      </div>
    </div>
  </section>

  <section class="sec band" id="faq" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="sec-head">
        <h2 id="faq-title">Questions</h2>
      </div>
      <div class="faq">
        <details><summary>What should I bring?</summary>
          <p>Two towels (one to sit on, one to dry off), a water bottle, flip-flops and a swimsuit. A wool felt sauna hat is welcome too. Wear it dry.</p></details>
        <details><summary>I have never been to a sauna. Can I come?</summary>
          <p>Yes. Start on a lower bench, where it is cooler, and keep your first rounds short. Our staff will show you the cold plunge and the rest area.</p></details>
        <details><summary>How cold is the plunge?</summary>
          <p>We post the water temperature at the front desk every day. Go in slowly, keep it short and get out if you feel unwell.</p></details>
        <details><summary>Can I book the whole sauna for a group?</summary>
          <p>Yes, on most evenings. Email us with the date, the time and how many people are coming.</p></details>
      </div>
    </div>
  </section>
</main>

<footer class="site-foot on-night">
  <div class="wrap">
    <div>
      <strong>Your Sauna Club</strong>
      <p>123 Example Road, Your Town, ST 00000</p>
    </div>
    <p>© 2026 Your Sauna Club</p>
    <p class="credit">Website template by <a href="https://diveluxsaunahat.com">DIVELUX</a>, makers of wool sauna hats.</p>
  </div>
</footer>
</body>
</html>
"""

MARK = """<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36"><title>Your Sauna Club mark</title>
<rect width="36" height="36" rx="6" fill="#1b1512"/>
<path d="M8 27h20" stroke="#f6f3ee" stroke-width="2.4" stroke-linecap="round"/>
<path d="M11 23h14l-2-6H13z" fill="#f6f3ee"/>
<path d="M14 13c1.6-1.3-1.6-2.7 0-4M18 13c1.6-1.3-1.6-2.7 0-4M22 13c1.6-1.3-1.6-2.7 0-4" fill="none" stroke="#f0762e" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

OFL_HEAD = """Fonts in this folder:

bricolage-grotesque-latin.woff2  Bricolage Grotesque (variable), Latin subset
  Copyright 2022 The Bricolage Grotesque Project Authors (https://github.com/ateliertriay/bricolage)
inter-latin.woff2                Inter (variable), Latin subset
  Copyright 2016 The Inter Project Authors (https://github.com/rsms/inter)

Both fonts are licensed under the SIL Open Font License, Version 1.1. The license text follows.
This license is copied below, and is also available with a FAQ at: https://openfontlicense.org

-----------------------------------------------------------
"""


def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
    S.write(os.path.join(OUT, "index.html"), HTML)
    S.write(os.path.join(OUT, "styles.css"), CSS)
    S.write(os.path.join(OUT, "assets", "mark.svg"), MARK)
    S.write(os.path.join(OUT, "assets", "favicon.svg"), MARK)
    src = open(os.path.join(S.ILLU, "lakeside-sauna.svg"), encoding="utf-8").read()
    src = src.replace("<title>", "<!-- From DIVELUX Sauna Illustrations, CC BY 4.0, https://diveluxsaunahat.com -->\n<title>", 1)
    S.write(os.path.join(OUT, "assets", "lakeside-sauna.svg"), src)
    shutil.copy(os.path.join(S.WOFF, "BricolageGrotesque-latin.woff2"), os.path.join(OUT, "fonts", "bricolage-grotesque-latin.woff2"))
    shutil.copy(os.path.join(S.WOFF, "Inter-latin.woff2"), os.path.join(OUT, "fonts", "inter-latin.woff2"))
    ofl = open("/root/dental/blender/license/spdx/OFL-1.1.txt", encoding="utf-8").read()
    S.write(os.path.join(OUT, "fonts", "OFL.txt"), OFL_HEAD + ofl)
    # one H1, every <img> has alt, every id referenced by aria-labelledby exists
    h = HTML
    assert len(re.findall(r"<h1\b", h)) == 1
    assert all("alt=" in m for m in re.findall(r"<img\b[^>]*>", h))
    ids = set(re.findall(r'\bid="([^"]+)"', h))
    for ref in re.findall(r'aria-labelledby="([^"]+)"', h):
        assert ref in ids, ref
    for ref in re.findall(r'href="#([^"]+)"', h):
        assert ref in ids, ref
    # contrast of the text pairs in styles.css
    pairs = [("#1b1512", "#f6f3ee"), ("#3d332c", "#f6f3ee"), ("#6f655c", "#f6f3ee"), ("#6f655c", "#efe9df"),
             ("#3d332c", "#efe9df"), ("#6f655c", "#fffdf9"), ("#1b1512", "#f0762e"), ("#1b1512", "#e8661b"),
             ("#f6f3ee", "#1c110b"), ("#d9cbbb", "#1c110b"), ("#d9cbbb", "#2a1b13"), ("#f6f3ee", "#2a1b13"),
             ("#f6f3ee", "#1b1512")]
    for a, b in pairs:
        r = S.contrast(a, b)
        print(f"contrast {a} on {b}: {r:.2f}", "OK" if r >= 4.5 else "FAIL")
        assert r >= 4.5


if __name__ == "__main__":
    main()
