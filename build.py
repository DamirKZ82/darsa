# -*- coding: utf-8 -*-
"""Собирает сайт darsa.kz из content.py: index.html (ru), kk/index.html, en/index.html.

Запуск:  python build.py
Править тексты — в content.py, разметку и стили — здесь.
"""

import html
import json
import os

from content import (C, GA_ID, GOOGLE_SITE_VERIFICATION, LANGS, ORIGIN,
                     PHONE, PHONE_HREF)

ROOT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------- токены

LIGHT = {
    "color-scheme": "light",
    "--bone": "#fbf9f4",
    "--surface": "#ffffff",
    "--ink": "#121216",
    "--text-2": "#43413c",
    "--mute": "#6f6c66",
    "--line": "#e3dfd5",
    "--duken": "#c1480b",
    "--toi": "#b31c44",
    "--bota": "#0f6a52",
    "--invert-bg": "#121216",
    "--invert-text": "#fbf9f4",
    "--invert-mute": "#b8b4ab",
    "--oyu-line": "#ddd7c9",
}

DARK = {
    "color-scheme": "dark",
    "--bone": "#121116",
    "--surface": "#1b1a21",
    "--ink": "#f3f0e9",
    "--text-2": "#c9c5bc",
    "--mute": "#9b968d",
    "--line": "#2e2c36",
    "--duken": "#b8460d",
    "--toi": "#9c1a3c",
    "--bota": "#0d5a46",
    "--invert-bg": "#1e1c25",
    "--invert-text": "#f3f0e9",
    "--invert-mute": "#a9a49b",
    "--oyu-line": "#3a3744",
}


def tokens(d, indent="  "):
    return "\n".join(f"{indent}{k}:{v};" for k, v in d.items())


CSS = """
:root{
__LIGHT__
  --display:"Rubik","Segoe UI",Arial,sans-serif;
  --body:"Manrope","Segoe UI",Arial,sans-serif;
  --mono:"JetBrains Mono",Consolas,monospace;
  --w:min(1160px,100% - 2*clamp(16px,5vw,48px));
  --ease:cubic-bezier(.32,.72,0,1);
}
:root[data-theme="dark"]{
__DARK__
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme]){
__DARK_MEDIA__
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bone);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased;transition:background .4s var(--ease),color .4s var(--ease)}
h1,h2,h3{margin:0;font-family:var(--display);font-weight:700;letter-spacing:-.03em;text-wrap:balance}
p{text-wrap:pretty}
a{color:inherit}
:focus-visible{outline:3px solid currentColor;outline-offset:3px;border-radius:4px}
.wrap{width:var(--w);margin-inline:auto}
.skip{position:absolute;left:-999px;top:8px;background:var(--invert-bg);color:var(--invert-text);padding:8px 12px;z-index:30}
.skip:focus{left:8px}

/* ornament band */
.oyu{display:block;width:100%;height:60px}
.oyu.tall{height:120px}
#oyu-l g{stroke:var(--oyu-line)}

/* nav */
.nav{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 0}
.brand{display:flex;align-items:center;gap:8px;text-decoration:none;font-family:var(--display);font-weight:700;letter-spacing:-.02em;white-space:nowrap}
.brand svg.logo{height:20px;width:auto;display:block;flex:none}
.nav ul{display:flex;gap:24px;list-style:none;margin:0;padding:0}
.nav ul a{text-decoration:none;font-size:14px;font-weight:500;padding:4px 0;border-bottom:2px solid transparent;transition:border-color .4s var(--ease)}
.nav ul a:hover{border-bottom-color:currentColor}
.navtools{display:flex;align-items:center;gap:8px}
.langs{display:flex;align-items:center;gap:2px;font-family:var(--mono);font-size:12px}
.langs a{text-decoration:none;padding:6px 8px;border-radius:999px;color:var(--mute);transition:color .3s var(--ease),background .3s var(--ease)}
.langs a:hover{color:var(--ink)}
.langs a[aria-current="page"]{color:var(--ink);background:var(--line)}
.iconbtn{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;flex:none;border-radius:999px;border:2px solid var(--line);background:transparent;color:inherit;cursor:pointer;transition:border-color .4s var(--ease),transform .3s var(--ease)}
.iconbtn:hover{border-color:currentColor}
.iconbtn:active{transform:scale(.94)}
.iconbtn svg{width:18px;height:18px;display:block}
:root[data-theme="dark"] .i-moon{display:none}
:root:not([data-theme="dark"]) .i-sun{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme]) .i-moon{display:none}:root:not([data-theme]) .i-sun{display:block}}
.btn{display:inline-flex;align-items:center;text-decoration:none;font-weight:600;font-size:16px;padding:12px 20px;border-radius:999px;background:var(--ink);color:var(--bone);transition:transform .5s var(--ease),opacity .5s var(--ease)}
.btn:hover{transform:translateY(-1px)}
.btn:active{transform:scale(.98)}
.btn.sm{font-size:14px;padding:8px 16px;white-space:nowrap}
.btn.light{background:#ffffff;color:#121216}
.ghost{text-decoration:none;font-weight:500;border-bottom:2px solid var(--line);transition:border-color .4s var(--ease)}
.ghost:hover{border-bottom-color:currentColor}
@media (max-width:980px){.nav ul{display:none}}
@media (max-width:560px){.brand .bt{display:none}.langs a{padding:6px}.btn.sm{font-size:13px;padding:8px 12px}}

/* hero */
.hero{padding:clamp(32px,6vw,72px) 0 0}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin:0 0 24px}
h1{font-size:clamp(36px,7vw,72px);line-height:1;max-width:680px}
h1 em{font-style:normal;display:block}
.hero .sub{max-width:600px;font-size:18px;color:var(--text-2);margin:24px 0 32px}
.cta{display:flex;flex-wrap:wrap;gap:12px 16px;align-items:center}
.proof{display:flex;flex-wrap:wrap;gap:8px 24px;margin:32px 0 40px;padding:0;list-style:none;font-family:var(--mono);font-size:12px;color:var(--mute)}
.band{display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;border-radius:20px;overflow:hidden}
.band div{padding:16px 20px 8px;color:#fff}
.band .n{font-family:var(--display);font-weight:700;font-size:clamp(20px,2.6vw,28px);letter-spacing:-.03em}
.band .k{font-family:var(--mono);font-size:12px;opacity:.85;display:block;margin-bottom:8px}
.band .d{background:var(--duken)}
.band .t{background:var(--toi)}
.band .b{background:var(--bota)}
@media (max-width:700px){.band{grid-template-columns:1fr}}

/* reveal */
.reveal{padding:clamp(56px,9vw,104px) 0}
.reveal p{font-family:var(--display);font-weight:500;font-size:clamp(26px,4.4vw,44px);line-height:1.18;letter-spacing:-.03em;max-width:680px;margin:0}
.reveal .w{color:var(--mute);opacity:.55;transition:color .7s var(--ease),opacity .7s var(--ease)}
.reveal .w.on{color:var(--ink);opacity:1}
@media (prefers-reduced-motion:reduce){.reveal .w{color:var(--ink);opacity:1}}

/* product fields */
.field{color:#fff;padding:clamp(40px,7vw,80px) 0;position:relative;overflow:hidden}
.field.d{background:var(--duken)}
.field.t{background:var(--toi)}
.field.b{background:var(--bota)}
.field .orn{position:absolute;inset:auto 0 0 0;opacity:.22;pointer-events:none}
.field .grid{display:grid;gap:clamp(24px,4vw,56px);grid-template-columns:1fr;position:relative}
.field .grid>*{min-width:0}
@media (min-width:900px){.field .grid{grid-template-columns:340px 1fr}}
.field h2{font-size:clamp(32px,5vw,52px);line-height:1}
.field .kk{font-family:var(--mono);font-size:12px;opacity:.85;margin:8px 0 0}
.field .lead{font-size:20px;font-weight:600;margin:0 0 24px;max-width:560px;line-height:1.3}
.facts{list-style:none;margin:0 0 24px;padding:0;display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));max-width:760px}
.facts li{border-top:2px solid rgba(255,255,255,.35);padding-top:12px}
.facts strong{display:block;font-weight:700;margin-bottom:4px}
.facts p{margin:0;font-size:14px;color:rgba(255,255,255,.88)}
.price{font-family:var(--mono);font-size:14px;margin:0 0 16px;color:rgba(255,255,255,.88)}
.price b{color:#fff;font-weight:500}
.note{font-family:var(--mono);font-size:12px;color:rgba(255,255,255,.82);margin:16px 0 0}
.pill{display:inline-block;font-family:var(--mono);font-size:12px;border:1.5px solid rgba(255,255,255,.5);border-radius:999px;padding:4px 12px;margin-bottom:16px}

/* steps + about + faq */
.section{padding:clamp(48px,8vw,88px) 0}
h2.sec{font-size:clamp(26px,3.6vw,38px);margin-bottom:12px}
.sec-lead{color:var(--mute);font-size:18px;max-width:600px;margin:0 0 40px}
.prose{max-width:680px;font-size:18px;margin:0 0 16px;color:var(--text-2)}
.prose:last-child{margin-bottom:0}
.steps{list-style:none;margin:0;padding:0;display:grid;gap:0}
.steps li{display:grid;grid-template-columns:64px 1fr;gap:16px;padding:24px 0;border-top:2px solid var(--line);align-items:start}
.steps .n{font-family:var(--display);font-weight:700;font-size:24px;color:var(--line)}
.steps h3{font-size:20px;margin-bottom:4px}
.steps p{margin:0;color:var(--text-2);max-width:600px}
details{border-top:2px solid var(--line);padding:20px 0}
details:last-of-type{border-bottom:2px solid var(--line)}
details summary{cursor:pointer;list-style:none;font-family:var(--display);font-weight:500;font-size:18px;letter-spacing:-.02em;display:flex;justify-content:space-between;gap:16px}
details summary::-webkit-details-marker{display:none}
details summary::after{content:"+";font-family:var(--mono);color:var(--mute)}
details[open] summary::after{content:"\\2212"}
details p{margin:12px 0 0;max-width:680px;color:var(--text-2)}

/* final */
.final{background:var(--invert-bg);color:var(--invert-text);padding:clamp(48px,8vw,96px) 0;position:relative;overflow:hidden}
.final .orn{position:absolute;inset:0 0 auto 0;opacity:.16}
.final h2{font-size:clamp(30px,5vw,52px);line-height:1.04;max-width:680px;position:relative}
.final p{max-width:560px;font-size:18px;color:var(--invert-mute);margin:16px 0 32px;position:relative}
.final .cta{position:relative}
footer{padding:32px 0 48px;font-size:14px;color:var(--mute)}
footer .row{display:flex;flex-wrap:wrap;gap:12px 32px;justify-content:space-between;align-items:baseline}
footer a{text-decoration:none}
footer a:hover{color:var(--ink)}
dl{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;font-family:var(--mono);font-size:12px;margin:0 0 24px}
dt{color:var(--mute)}dd{margin:0}

@media (prefers-reduced-motion:no-preference){
  [data-rise]{opacity:0;transform:translateY(16px);filter:blur(6px);transition:opacity .8s var(--ease),transform .8s var(--ease),filter .8s var(--ease)}
  [data-rise].in{opacity:1;transform:none;filter:none}
}
"""

HEAD_SCRIPT = """(function(){try{var s=localStorage.getItem('darsa-theme');\
var t=s==='dark'||s==='light'?s:(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');\
document.documentElement.setAttribute('data-theme',t);}catch(e){}})();"""

BODY_SCRIPT = """
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  var KEY = 'darsa-theme';

  /* theme */
  var btn = document.getElementById('theme-toggle');
  function current(){
    var a = root.getAttribute('data-theme');
    if (a === 'dark' || a === 'light') return a;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function apply(t){
    root.setAttribute('data-theme', t);
    if (btn) btn.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', t === 'dark' ? '#121116' : '#fbf9f4');
  }
  apply(current());
  if (btn) btn.addEventListener('click', function(){
    var next = current() === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem(KEY, next); } catch (e) {}
    apply(next);
  });
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e){
    var stored = null;
    try { stored = localStorage.getItem(KEY); } catch (err) {}
    if (stored !== 'dark' && stored !== 'light') apply(e.matches ? 'dark' : 'light');
  });

  /* word-by-word tagline */
  var t = document.querySelector('[data-reveal]');
  if (t) {
    var words = t.textContent.trim().split(/\\s+/);
    t.textContent = '';
    words.forEach(function(w, i){
      var s = document.createElement('span');
      s.className = 'w'; s.textContent = w;
      t.appendChild(s);
      if (i < words.length - 1) t.appendChild(document.createTextNode(' '));
    });
    if (reduce) { t.querySelectorAll('.w').forEach(function(s){ s.classList.add('on'); }); }
    else {
      var wo = new IntersectionObserver(function(entries){
        entries.forEach(function(e){
          if (!e.isIntersecting) return;
          var spans = Array.prototype.slice.call(t.querySelectorAll('.w'));
          var idx = spans.indexOf(e.target);
          setTimeout(function(){ e.target.classList.add('on'); }, idx * 55);
          wo.unobserve(e.target);
        });
      }, { rootMargin: '-20% 0px -35% 0px' });
      t.querySelectorAll('.w').forEach(function(s){ wo.observe(s); });
    }
  }

  /* scroll reveal */
  if (!reduce) {
    var els = document.querySelectorAll('.field .grid > *, .steps li, .final h2, .final p, .band');
    els.forEach(function(el){ el.setAttribute('data-rise',''); });
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    els.forEach(function(el){ io.observe(el); });
  }
})();
"""

LOGO = ('<svg class="logo" viewBox="0 0 48 40" aria-hidden="true">'
        '<path d="M0 0 H42 A6 6 0 0 1 42 12 H0 Z" fill="#d1500d"/>'
        '<path d="M0 14 H23 A6 6 0 0 1 23 26 H0 Z" fill="#b31c44"/>'
        '<path d="M0 28 H32 A6 6 0 0 1 32 40 H0 Z" fill="#0f6a52"/></svg>')

PATTERNS = """<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
  <defs>
    <pattern id="oyu-w" width="120" height="60" patternUnits="userSpaceOnUse">
      <g fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round">
        <path d="M4 58 C 4 26, 26 14, 38 30 C 46 41, 32 52, 26 42"/>
        <path d="M116 58 C 116 26, 94 14, 82 30 C 74 41, 88 52, 94 42"/>
        <path d="M60 58 C 60 40, 46 22, 60 6 C 74 22, 60 40, 60 58"/>
      </g>
    </pattern>
    <pattern id="oyu-l" width="120" height="60" patternUnits="userSpaceOnUse">
      <g fill="none" stroke-width="3" stroke-linecap="round">
        <path d="M4 58 C 4 26, 26 14, 38 30 C 46 41, 32 52, 26 42"/>
        <path d="M116 58 C 116 26, 94 14, 82 30 C 74 41, 88 52, 94 42"/>
        <path d="M60 58 C 60 40, 46 22, 60 6 C 74 22, 60 40, 60 58"/>
      </g>
    </pattern>
  </defs>
</svg>"""

SUN = ('<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/>'
       '<path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>')
MOON = ('<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a6.8 6.8 0 0 0 10.5 10.5z"/></svg>')


GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=__ID__"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '__ID__');
</script>"""


def head_tags():
    """Подтверждение прав Search Console и счётчик GA4 — только если заполнены."""
    out = []
    if GOOGLE_SITE_VERIFICATION:
        out.append(
            '<meta name="google-site-verification" content="'
            + html.escape(GOOGLE_SITE_VERIFICATION) + '">')
    if GA_ID:
        out.append(GTAG.replace("__ID__", GA_ID))
    return ("\n".join(out) + "\n") if out else ""


def e(s):
    return html.escape(str(s), quote=False)


def field(cls, anchor, name, d):
    pill = f'\n      <p class="pill">{e(d["pill"])}</p>' if d.get("pill") else ""
    price = f'\n      <p class="price">{d["price"]}</p>' if d.get("price") else ""
    note = f'\n      <p class="note">{e(d["note"])}</p>' if d.get("note") else ""
    href = "https://iduken.kz" if anchor == "iduken" else PHONE_HREF
    rel = ' rel="noopener"' if anchor == "iduken" else ""
    facts = "\n".join(
        f'        <li><strong>{e(t)}</strong><p>{e(p)}</p></li>' for t, p in d["facts"]
    )
    return f"""<section class="field {cls}" id="{anchor}">
  <svg class="oyu tall orn" aria-hidden="true"><rect width="100%" height="100%" fill="url(#oyu-w)"/></svg>
  <div class="wrap grid">
    <div>
      <h2>{name}</h2>
      <p class="kk">{e(d["gloss"])}</p>
    </div>
    <div>{pill}
      <p class="lead">{e(d["lead"])}</p>
      <ul class="facts">
{facts}
      </ul>{price}
      <a class="btn light sm" href="{href}"{rel}>{e(d["btn"])}</a>{note}
    </div>
  </div>
</section>"""


def jsonld(lang, c):
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "DARSA Solutions",
        "legalName": c["footer"][0][1],
        "url": ORIGIN + "/",
        "logo": ORIGIN + "/logo.svg",
        "telephone": PHONE,
        "address": {"@type": "PostalAddress", "addressCountry": "KZ"},
        "description": c["desc"],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": lang,
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in c["faq"]
        ],
    }
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    return (f'<script type="application/ld+json">{dump(org)}</script>\n'
            f'<script type="application/ld+json">{dump(faq)}</script>')


def render(lang):
    c = C[lang]
    prefix = dict((l, p) for l, p, _ in LANGS)[lang]
    canonical = f"{ORIGIN}/{prefix}"

    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}/{p}">' for l, p, _ in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'

    langs = "\n    ".join(
        '<a href="/{p}" lang="{l}" hreflang="{l}"{cur}>{lab}</a>'.format(
            p=p, l=l, lab=lab, cur=' aria-current="page"' if l == lang else "")
        for l, p, lab in LANGS
    )

    proof = "\n".join(f'    <li>· {e(x)}</li>' for x in c["proof"])
    band = "\n".join(
        f'    <div class="{cls}"><span class="n">{n}</span><span class="k">{e(g)}</span></div>'
        for cls, (n, g) in zip(["d", "t", "b"], c["band"])
    )
    steps = "\n".join(
        f'    <li><span class="n">0{i}</span><div><h3>{e(h)}</h3><p>{e(p)}</p></div></li>'
        for i, (h, p) in enumerate(c["steps"], 1)
    )
    about = "\n  ".join(f'<p class="prose">{e(p)}</p>' for p in c["about_p"])
    faq = "\n  ".join(
        '<details{op}><summary>{q}</summary><p>{a}</p></details>'.format(
            op=" open" if i == 0 else "", q=e(q), a=e(a))
        for i, (q, a) in enumerate(c["faq"])
    )
    dl = "\n    ".join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in c["footer"])

    css = (CSS.replace("__LIGHT__", tokens(LIGHT))
              .replace("__DARK__", tokens(DARK))
              .replace("__DARK_MEDIA__", tokens(DARK, "    ")))

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_tags()}<title>{e(c["title"])}</title>
<meta name="description" content="{html.escape(c["desc"])}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#fbf9f4">
<link rel="canonical" href="{canonical}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{c["og_locale"]}">
<meta property="og:title" content="{html.escape(c["og_title"])}">
<meta property="og:description" content="{html.escape(c["og_desc"])}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@500;700&family=Manrope:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script>{HEAD_SCRIPT}</script>
<style>{css}</style>
{jsonld(lang, c)}
</head>
<body>
<a class="skip" href="#main">{e(c["skip"])}</a>

{PATTERNS}

<header class="wrap nav">
  <a class="brand" href="#top">{LOGO}<span class="bt">Darsa Solutions</span></a>
  <nav aria-label="{e(c["nav_label"])}"><ul>
    <li><a href="#iduken">iDüken</a></li>
    <li><a href="#toiapp">ToiApp</a></li>
    <li><a href="#bota">Bota</a></li>
    <li><a href="#faq">{e(c["nav_faq"])}</a></li>
  </ul></nav>
  <div class="navtools">
    <nav class="langs" aria-label="{e(c["lang_label"])}">
    {langs}
    </nav>
    <button class="iconbtn" id="theme-toggle" type="button" aria-pressed="false" aria-label="{e(c["theme_label"])}" title="{e(c["theme_label"])}">{SUN}{MOON}</button>
    <a class="btn sm" href="{PHONE_HREF}">{e(c["nav_call"])}</a>
  </div>
</header>

<main id="main">
<section class="hero wrap" id="top">
  <p class="eyebrow">{e(c["eyebrow"])}</p>
  <h1>{c["h1"]}</h1>
  <p class="sub">{e(c["sub"])}</p>
  <div class="cta">
    <a class="btn" href="#iduken">{e(c["cta"])}</a>
    <a class="ghost" href="{PHONE_HREF}">{PHONE}</a>
  </div>
  <ul class="proof">
{proof}
  </ul>

  <div class="band">
{band}
  </div>
  <svg class="oyu" style="margin-top:16px" aria-hidden="true"><rect width="100%" height="100%" fill="url(#oyu-l)"/></svg>
</section>

<section class="reveal wrap">
  <p data-reveal>{e(c["reveal"])}</p>
</section>

{field("d", "iduken", "iDüken", c["iduken"])}

{field("t", "toiapp", "ToiApp", c["toiapp"])}

{field("b", "bota", "Bota", c["bota"])}

<section class="section wrap">
  <h2 class="sec">{e(c["steps_title"])}</h2>
  <p class="sec-lead">{e(c["steps_lead"])}</p>
  <ol class="steps">
{steps}
  </ol>
</section>

<section class="section wrap" id="about">
  <h2 class="sec">{e(c["about_title"])}</h2>
  <p class="sec-lead">{e(c["about_lead"])}</p>
  {about}
</section>

<section class="section wrap" id="faq">
  <h2 class="sec">{e(c["faq_title"])}</h2>
  <p class="sec-lead">{e(c["faq_lead"])}</p>
  {faq}
</section>

<section class="final" id="contacts">
  <svg class="oyu tall orn" aria-hidden="true"><rect width="100%" height="100%" fill="url(#oyu-w)"/></svg>
  <div class="wrap">
    <h2>{e(c["final_h"])}</h2>
    <p>{e(c["final_p"])}</p>
    <div class="cta">
      <a class="btn light" href="{PHONE_HREF}">{e(c["final_btn"])}</a>
    </div>
  </div>
</section>
</main>

<footer class="wrap">
  <dl>
    {dl}
  </dl>
  <div class="row">
    <span>{e(c["copyright"])}</span>
    <span><a href="#top">{e(c["top"])}</a></span>
  </div>
</footer>

<script>{BODY_SCRIPT}</script>
</body>
</html>
"""


def main():
    for lang, prefix, _ in LANGS:
        out = os.path.join(ROOT, prefix, "index.html") if prefix else os.path.join(ROOT, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(render(lang))
        print(f"{lang}: {os.path.relpath(out, ROOT)} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
