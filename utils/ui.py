"""Custom UI component system for Magnetism Lab.

This module is the app's design layer. It centralizes one stylesheet and a set
of small, composable helpers (hero, nav, cards, callouts, plot shells, footer…)
so the page modules read like a layout description instead of a wall of HTML.

Design choices that keep it maintainable:

* All colors live as CSS custom properties in ``:root`` and the rest of the
  stylesheet references them via ``var(--ml-…)``. That means the CSS is plain
  text (no Python ``f``-string brace-escaping) and lives in a few readable
  chunks joined once in :func:`inject_global_styles`.
* Presentation-only pieces are rendered as custom HTML. Interactive Streamlit
  widgets are wrapped in styled shells (bordered containers / custom headers)
  rather than embedded in HTML, so interactivity never breaks.
"""
from __future__ import annotations

from contextlib import contextmanager
from html import escape

import streamlit as st

# --- Stylesheet, in readable chunks --------------------------------------
_CSS_TOKENS = """
:root {
    --ml-ink: #0b1220;
    --ml-body: #475569;
    --ml-muted: #6b7a90;
    --ml-primary: #4f46e5;
    --ml-primary-dk: #4338ca;
    --ml-primary-soft: #eef2ff;
    --ml-accent: #7c3aed;
    --ml-line: #e7eaf3;
    --ml-surface: #ffffff;
    --ml-shadow: 0 18px 44px -28px rgba(15,23,42,.45);
    --ml-shadow-lg: 0 30px 60px -30px rgba(79,70,229,.55);
    --ml-radius: 22px;
}
"""

_CSS_BASE = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Fraunces:opsz,wght@9..144,500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Soft, product-like page background. */
.stApp {
    background:
        radial-gradient(1100px 560px at 8% -10%, #e9edff 0%, rgba(233,237,255,0) 55%),
        radial-gradient(900px 480px at 108% -6%, #f3ecff 0%, rgba(243,236,255,0) 52%),
        linear-gradient(180deg, #fbfcff 0%, #f4f7fd 100%);
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container { padding-top: 1.4rem; padding-bottom: 1rem; max-width: 1080px; }

h1, h2, h3, h4 { color: var(--ml-ink); letter-spacing: -0.015em; }
a { color: var(--ml-primary); text-decoration: none; }

.ml-divider {
    height: 1px; border: 0; margin: 2.2rem 0 1.4rem;
    background: linear-gradient(90deg, rgba(79,70,229,0), var(--ml-line) 18%, var(--ml-line) 82%, rgba(79,70,229,0));
}
.ml-eyebrow {
    display:inline-block; text-transform:uppercase; letter-spacing:.13em;
    font-size:.72rem; font-weight:800; color:var(--ml-primary);
    background:var(--ml-primary-soft); padding:.22rem .6rem; border-radius:7px;
}
.ml-section { margin: 0 0 1rem; }
.ml-section h2 { font-size: 1.7rem; font-weight: 800; margin:.5rem 0 0; }
.ml-section p { color: var(--ml-body); margin:.35rem 0 0; font-size: 1.02rem; max-width: 760px; line-height:1.55; }
"""

_CSS_NAV = """
.ml-brand {
    display:flex; align-items:center; gap:.7rem; padding:.2rem 0 .1rem;
}
.ml-brand .ml-logo {
    width:40px; height:40px; border-radius:12px; display:flex; align-items:center;
    justify-content:center; font-size:1.4rem;
    background: linear-gradient(135deg, var(--ml-primary), var(--ml-accent));
    box-shadow: var(--ml-shadow-lg);
}
.ml-brand .ml-brandname { font-weight:800; font-size:1.18rem; color:var(--ml-ink); line-height:1; }
.ml-brand .ml-brandtag { font-size:.78rem; color:var(--ml-muted); font-weight:600; }
.ml-navwrap { margin:.2rem 0 .6rem; }
"""

_CSS_HERO = """
.ml-hero {
    position: relative; overflow: hidden; color:#fff;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 52%, #9333ea 100%);
    border-radius: 28px; padding: 3.1rem 2.7rem; margin: .4rem 0 1.4rem;
    box-shadow: var(--ml-shadow-lg);
}
.ml-hero::after {
    content:""; position:absolute; right:-110px; top:-110px; width:360px; height:360px;
    border-radius:50%; background: radial-gradient(circle at center, rgba(255,255,255,.22), rgba(255,255,255,0) 70%);
}
.ml-hero::before {
    content:""; position:absolute; left:-80px; bottom:-120px; width:300px; height:300px;
    border-radius:50%; background: radial-gradient(circle at center, rgba(147,197,253,.25), rgba(147,197,253,0) 70%);
}
.ml-hero .ml-kicker {
    display:inline-block; font-size:.74rem; font-weight:700; letter-spacing:.14em;
    text-transform:uppercase; background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.34);
    padding:.28rem .7rem; border-radius:999px; margin-bottom:1rem; backdrop-filter: blur(4px);
}
.ml-hero h1 { font-size:3.1rem; font-weight:900; margin:0 0 .55rem; color:#fff; line-height:1.04; }
.ml-hero .ml-sub { font-size:1.2rem; font-weight:600; opacity:.97; margin-bottom:.7rem; max-width:720px; }
.ml-hero .ml-desc { font-size:1.02rem; opacity:.9; max-width:650px; line-height:1.6; }
.ml-badges { display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.4rem; }
.ml-badge {
    display:inline-flex; align-items:center; gap:.35rem; font-size:.83rem; font-weight:600;
    background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.36);
    border-radius:999px; padding:.36rem .9rem; backdrop-filter: blur(4px);
}

/* Compact module hero used on inner pages. */
.ml-pagehero {
    position:relative; overflow:hidden; color:#fff; border-radius:24px;
    padding:2rem 2.1rem; margin:.4rem 0 1.3rem; box-shadow: var(--ml-shadow-lg);
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
}
.ml-pagehero.green { background: linear-gradient(135deg, #0ea5e9, #4f46e5); }
.ml-pagehero.amber { background: linear-gradient(135deg, #f59e0b, #db2777); }
.ml-pagehero.teal  { background: linear-gradient(135deg, #10b981, #0ea5e9); }
.ml-pagehero .ml-ph-icon { font-size:2rem; }
.ml-pagehero h1 { font-size:2rem; font-weight:800; color:#fff; margin:.4rem 0 .3rem; }
.ml-pagehero p { font-size:1.02rem; opacity:.94; margin:0; max-width:680px; line-height:1.5; }
"""

_CSS_CARDS = """
.ml-grid { display:grid; gap:1rem; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); }
.ml-grid-2 { display:grid; gap:1rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }

.ml-card {
    background:var(--ml-surface); border:1px solid var(--ml-line); border-radius:18px;
    padding:1.35rem 1.4rem; box-shadow: var(--ml-shadow); height:100%;
    transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
}
.ml-card:hover { transform: translateY(-4px); box-shadow: var(--ml-shadow-lg); border-color:#d7dbf2; }
.ml-card .ml-icon {
    display:inline-flex; align-items:center; justify-content:center; width:48px; height:48px;
    border-radius:14px; font-size:1.6rem; background:var(--ml-primary-soft);
}
.ml-card h3 { font-size:1.14rem; font-weight:800; margin:.7rem 0 .35rem; }
.ml-card p { color:var(--ml-body); font-size:.94rem; line-height:1.55; margin:0; }
.ml-concepts { display:flex; flex-wrap:wrap; gap:.4rem; margin-top:.85rem; }
.ml-concepts span {
    font-size:.72rem; font-weight:700; color:var(--ml-muted);
    border:1px solid var(--ml-line); border-radius:8px; padding:.14rem .55rem;
}

/* Timeline / learning path */
.ml-step { display:flex; gap:1rem; align-items:flex-start; margin-bottom:1rem; position:relative; }
.ml-step .ml-num {
    flex:0 0 auto; width:38px; height:38px; border-radius:12px; color:#fff; font-weight:800;
    display:flex; align-items:center; justify-content:center; font-size:1rem;
    background: linear-gradient(135deg, var(--ml-primary), var(--ml-accent));
    box-shadow: 0 10px 18px -10px rgba(79,70,229,.7);
}
.ml-step .ml-step-body h4 { margin:0; font-size:1.05rem; font-weight:700; }
.ml-step .ml-step-body p { margin:.15rem 0 0; color:var(--ml-body); font-size:.93rem; }

/* Concept / value chips */
.ml-chips { display:flex; flex-wrap:wrap; gap:.5rem; margin:.4rem 0 .9rem; }
.ml-chip {
    background:#fff; color:var(--ml-primary); border:1px solid var(--ml-line);
    border-radius:10px; padding:.4rem .8rem; font-size:.86rem; font-weight:700;
}
.ml-chip b { color:var(--ml-ink); }
"""

_CSS_FORMULA = """
.ml-formula-grid { display:grid; gap:.85rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin:.3rem 0 .6rem; }
.ml-formula {
    text-align:center; color:#e8e9f6; border-radius:18px; padding:1.2rem 1.3rem;
    background: linear-gradient(160deg, #0b1020 0%, #211a4d 100%);
    border:1px solid rgba(124,58,237,.4); box-shadow: 0 18px 36px -26px rgba(30,27,75,.95);
}
.ml-formula .ml-fname { font-size:.72rem; text-transform:uppercase; letter-spacing:.12em; color:#a5b4fc; font-weight:800; }
.ml-formula .ml-feq {
    font-family:'Fraunces', Georgia, serif; font-size:1.8rem; font-weight:600; color:#fff; margin:.45rem 0;
}
.ml-formula .ml-fdesc { font-size:.85rem; color:#c7d2fe; line-height:1.45; }
"""

_CSS_CALLOUT = """
.ml-callout {
    display:flex; gap:.9rem; align-items:flex-start; background:#fff;
    border:1px solid var(--ml-line); border-left:5px solid var(--ml-primary);
    border-radius:16px; padding:1rem 1.15rem; margin:.5rem 0 1rem; box-shadow: var(--ml-shadow);
}
.ml-callout .ml-co-icon { font-size:1.35rem; line-height:1.35; }
.ml-callout .ml-co-title { font-weight:800; color:var(--ml-ink); font-size:.96rem; margin-bottom:.15rem; }
.ml-callout .ml-co-body { color:var(--ml-body); font-size:.94rem; line-height:1.6; }
.ml-callout .ml-co-body b { color:var(--ml-ink); }
.ml-callout--why { border-left-color:#4f46e5; }
.ml-callout--intuition { border-left-color:#7c3aed; }
.ml-callout--mistake { border-left-color:#dc2626; }
.ml-callout--predict { border-left-color:#2563eb; }
.ml-callout--edge { border-left-color:#64748b; }
.ml-callout--info { border-left-color:#0ea5e9; }

/* Step list inside a card */
.ml-steplist { counter-reset: ml; list-style:none; margin:0; padding:0; }
.ml-steplist li {
    position:relative; padding:.45rem 0 .45rem 2.3rem; color:var(--ml-body); font-size:.96rem;
    border-bottom:1px dashed var(--ml-line);
}
.ml-steplist li:last-child { border-bottom:0; }
.ml-steplist li::before {
    counter-increment: ml; content: counter(ml); position:absolute; left:0; top:.4rem;
    width:1.5rem; height:1.5rem; border-radius:8px; color:#fff; font-size:.8rem; font-weight:800;
    display:flex; align-items:center; justify-content:center;
    background: linear-gradient(135deg, var(--ml-primary), var(--ml-accent));
}
.ml-cardbox {
    background:#fff; border:1px solid var(--ml-line); border-radius:18px;
    padding:1.1rem 1.3rem; box-shadow: var(--ml-shadow); margin:.3rem 0 1rem;
}
.ml-cardbox h4 { margin:0 0 .5rem; font-size:1.05rem; font-weight:800; }
"""

_CSS_STATS = """
.ml-stats { display:grid; gap:.85rem; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); margin:.3rem 0 1rem; }
.ml-stat { border-radius:18px; padding:1.05rem 1.15rem; color:#fff; box-shadow: var(--ml-shadow-lg);
           background: linear-gradient(135deg, var(--ml-primary), var(--ml-accent)); }
.ml-stat .ml-stat-label { font-size:.74rem; text-transform:uppercase; letter-spacing:.09em; opacity:.92; font-weight:800; }
.ml-stat .ml-stat-value { font-size:1.95rem; font-weight:900; line-height:1.1; margin-top:.25rem; }
.ml-stat .ml-stat-sub { font-size:.78rem; opacity:.9; margin-top:.15rem; }
.ml-stat.alt  { background: linear-gradient(135deg, #0ea5e9, #6366f1); }
.ml-stat.warm { background: linear-gradient(135deg, #f59e0b, #ef4444); }
.ml-stat.cool { background: linear-gradient(135deg, #10b981, #0ea5e9); }
.ml-stat.slate{ background: linear-gradient(135deg, #334155, #4f46e5); }
"""

_CSS_PRACTICE = """
.ml-qhead { display:flex; flex-direction:column; gap:.55rem; margin-bottom:.2rem; }
.ml-qbadges { display:flex; flex-wrap:wrap; gap:.45rem; }
.ml-pill { display:inline-block; border-radius:999px; padding:.22rem .7rem; font-size:.74rem; font-weight:800; }
.ml-pill.easy { background:#dcfce7; color:#15803d; }
.ml-pill.medium { background:#fef3c7; color:#b45309; }
.ml-pill.challenge { background:#fee2e2; color:#b91c1c; }
.ml-pill.topic { background:var(--ml-primary-soft); color:var(--ml-primary); }
.ml-pill.muted { background:#f1f5f9; color:#64748b; }
.ml-qtext { font-size:1.05rem; font-weight:700; color:var(--ml-ink); line-height:1.4; }

.ml-hint { background:#fffbeb; border:1px solid #fde68a; border-radius:12px; padding:.7rem .9rem;
           color:#92400e; font-size:.9rem; margin:.4rem 0; }
.ml-hint b { color:#78350f; }
.ml-result { border-radius:14px; padding:.85rem 1rem; margin:.5rem 0 .2rem; font-size:.94rem; }
.ml-result.ok { background:#ecfdf5; border:1px solid #a7f3d0; color:#065f46; }
.ml-result.no { background:#fef2f2; border:1px solid #fecaca; color:#991b1b; }
.ml-result .ml-concept { display:block; margin-top:.35rem; font-size:.8rem; color:var(--ml-muted); font-weight:700; }
"""

_CSS_TABLE = """
.ml-table { width:100%; border-collapse:separate; border-spacing:0; border:1px solid var(--ml-line);
            border-radius:14px; overflow:hidden; box-shadow: var(--ml-shadow); background:#fff; }
.ml-table th { text-align:left; font-size:.78rem; text-transform:uppercase; letter-spacing:.06em;
               color:var(--ml-muted); background:#f8fafc; padding:.7rem 1rem; }
.ml-table td { padding:.7rem 1rem; border-top:1px solid var(--ml-line); color:var(--ml-body); font-size:.95rem; }
.ml-table td.mono { font-family:'Fraunces', Georgia, serif; color:var(--ml-ink); font-weight:600; }
"""

_CSS_PLOT = """
.ml-plot-head { margin-bottom:.2rem; }
.ml-plot-title { font-weight:800; font-size:1.05rem; color:var(--ml-ink); }
.ml-plot-cap { color:var(--ml-muted); font-size:.86rem; margin-top:.1rem; }
"""

_CSS_FOOTER = """
.ml-footer { margin-top:2.2rem; padding:1.4rem 1.6rem; border-radius:18px; border:1px solid var(--ml-line);
             background:#fff; box-shadow: var(--ml-shadow); display:flex; flex-wrap:wrap; gap:.6rem;
             align-items:center; justify-content:space-between; }
.ml-footer .ml-f-brand { font-weight:800; color:var(--ml-ink); }
.ml-footer .ml-f-meta { color:var(--ml-muted); font-size:.86rem; }
"""

_CSS_WIDGETS = """
/* Buttons */
.stButton > button {
    border-radius:12px; font-weight:700; border:1px solid var(--ml-line);
    padding:.5rem 1rem; background:#fff; color:var(--ml-ink); transition: all .15s ease;
}
.stButton > button:hover { border-color:var(--ml-primary); color:var(--ml-primary); transform: translateY(-1px); }
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--ml-primary), var(--ml-accent)); color:#fff; border:0;
    box-shadow: 0 14px 26px -16px rgba(79,70,229,.85);
}
.stButton > button[kind="primary"]:hover { filter: brightness(1.06); color:#fff; }

/* Bordered containers used as control / plot shells */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius:20px !important; border-color:var(--ml-line) !important;
    background:#fff; box-shadow: var(--ml-shadow);
}
[data-testid="stVerticalBlockBorderWrapper"] > div { padding-top:.2rem; }

/* Expanders as cards */
[data-testid="stExpander"] {
    border:1px solid var(--ml-line) !important; border-radius:16px !important; background:#fff;
    box-shadow: var(--ml-shadow); overflow:hidden; margin-bottom:.7rem;
}
[data-testid="stExpander"] summary { font-weight:700; }
[data-testid="stExpander"] summary:hover { color:var(--ml-primary); }

/* Inputs */
[data-testid="stRadio"] label, [data-testid="stSelectbox"] label,
[data-testid="stSlider"] label, [data-testid="stNumberInput"] label { font-weight:600; color:var(--ml-body); }

/* Sidebar */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #ffffff, #f3f6fd); border-right:1px solid var(--ml-line); }

@media (max-width: 640px) {
    .ml-hero { padding:2.1rem 1.4rem; border-radius:20px; }
    .ml-hero h1 { font-size:2.2rem; }
    .ml-hero .ml-sub { font-size:1.04rem; }
    .block-container { padding-left:.7rem; padding-right:.7rem; }
}
"""

_ALL_CSS = (
    _CSS_TOKENS + _CSS_BASE + _CSS_NAV + _CSS_HERO + _CSS_CARDS + _CSS_FORMULA
    + _CSS_CALLOUT + _CSS_STATS + _CSS_PRACTICE + _CSS_TABLE + _CSS_PLOT
    + _CSS_FOOTER + _CSS_WIDGETS
)


def inject_global_styles() -> None:
    """Inject the app-wide stylesheet once. Safe to call on every render."""
    st.markdown(f"<style>{_ALL_CSS}</style>", unsafe_allow_html=True)


# Backwards-compatible alias for older call sites.
inject_global_css = inject_global_styles


# --- Navigation ----------------------------------------------------------
def navigate_to(page: str) -> None:
    """Set the active page (used by card / nav buttons via ``on_click``)."""
    st.session_state["page"] = page


def top_nav(pages: list[str], active: str) -> None:
    """Render the brand bar plus a row of nav buttons that switch pages.

    The active page's button is highlighted. Navigation goes through
    :func:`navigate_to`, an ``on_click`` callback that fires before the page is
    rebuilt, so session-state routing stays intact.
    """
    st.markdown(
        '<div class="ml-brand"><div class="ml-logo">🧲</div>'
        '<div><div class="ml-brandname">Magnetism Lab</div>'
        '<div class="ml-brandtag">Interactive E&M for first-year physics</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="ml-navwrap"></div>', unsafe_allow_html=True)
    cols = st.columns(len(pages))
    for col, page in zip(cols, pages):
        with col:
            st.button(
                page, key=f"topnav_{page}", use_container_width=True,
                type="primary" if page == active else "secondary",
                on_click=navigate_to, args=(page,),
            )
    divider()


# --- Layout helpers ------------------------------------------------------
def hero_section(title: str, subtitle: str, description: str,
                 badges: list[str] | None = None, kicker: str | None = None) -> None:
    """Render the big landing hero with title, subtitle, blurb and badges."""
    kicker_html = f'<div class="ml-kicker">{escape(kicker)}</div>' if kicker else ""
    badge_html = ""
    if badges:
        chips = "".join(f'<span class="ml-badge">✦ {escape(b)}</span>' for b in badges)
        badge_html = f'<div class="ml-badges">{chips}</div>'
    st.markdown(
        f'<div class="ml-hero">{kicker_html}<h1>{escape(title)}</h1>'
        f'<div class="ml-sub">{escape(subtitle)}</div>'
        f'<div class="ml-desc">{escape(description)}</div>{badge_html}</div>',
        unsafe_allow_html=True,
    )


# Older alias.
hero = hero_section


def page_hero(icon: str, title: str, subtitle: str, theme: str = "") -> None:
    """Render a compact module-page hero header.

    ``theme`` is one of ``""``, ``green``, ``amber`` or ``teal``.
    """
    st.markdown(
        f'<div class="ml-pagehero {theme}"><div class="ml-ph-icon">{escape(icon)}</div>'
        f'<h1>{escape(title)}</h1><p>{escape(subtitle)}</p></div>',
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str | None = None,
                   eyebrow: str | None = None) -> None:
    """Render a section heading with an optional eyebrow and subtitle."""
    eb = f'<span class="ml-eyebrow">{escape(eyebrow)}</span><br>' if eyebrow else ""
    sub = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f'<div class="ml-section">{eb}<h2>{escape(title)}</h2>{sub}</div>',
        unsafe_allow_html=True,
    )


def divider() -> None:
    """Render a soft section divider."""
    st.markdown('<hr class="ml-divider">', unsafe_allow_html=True)


# --- Cards ---------------------------------------------------------------
def module_card(icon: str, title: str, body: str,
                concepts: list[str] | None = None) -> str:
    """Return the HTML for one module/info card (no interactivity)."""
    icon_html = f'<div class="ml-icon">{escape(icon)}</div>' if icon else ""
    concepts_html = ""
    if concepts:
        pills = "".join(f"<span>{escape(c)}</span>" for c in concepts)
        concepts_html = f'<div class="ml-concepts">{pills}</div>'
    return (
        f'<div class="ml-card">{icon_html}<h3>{escape(title)}</h3>'
        f'<p>{escape(body)}</p>{concepts_html}</div>'
    )


def card_grid(cards: list[dict], wide: bool = False) -> None:
    """Render a responsive grid of static cards (icon/title/body/concepts)."""
    cls = "ml-grid-2" if wide else "ml-grid"
    items = "".join(
        module_card(c.get("icon", ""), c["title"], c["body"], c.get("concepts"))
        for c in cards
    )
    st.markdown(f'<div class="{cls}">{items}</div>', unsafe_allow_html=True)


def module_cards(cards: list[dict], columns: int = 2) -> None:
    """Render large module cards, each with a real navigation CTA button.

    Each dict needs ``icon``, ``title``, ``body``, ``target`` (page label) and
    an optional ``concepts`` list.
    """
    for start in range(0, len(cards), columns):
        row = cards[start:start + columns]
        cols = st.columns(len(row), gap="medium")
        for col, c in zip(cols, row):
            with col:
                st.markdown(module_card(c.get("icon", ""), c["title"], c["body"],
                                        c.get("concepts")), unsafe_allow_html=True)
                st.button("Start module  →", key=f"nav_{c['target']}",
                          type="primary", use_container_width=True,
                          on_click=navigate_to, args=(c["target"],))


def learning_path(steps: list[tuple[str, str]]) -> None:
    """Render a numbered timeline of (title, description) steps."""
    rows = "".join(
        f'<div class="ml-step"><div class="ml-num">{i}</div>'
        f'<div class="ml-step-body"><h4>{escape(t)}</h4><p>{escape(d)}</p></div></div>'
        for i, (t, d) in enumerate(steps, start=1)
    )
    st.markdown(rows, unsafe_allow_html=True)


def steps_card(title: str, steps: list[str]) -> None:
    """Render a titled card containing a numbered step list."""
    items = "".join(f"<li>{s}</li>" for s in steps)
    st.markdown(
        f'<div class="ml-cardbox"><h4>{escape(title)}</h4>'
        f'<ol class="ml-steplist">{items}</ol></div>',
        unsafe_allow_html=True,
    )


# --- Formulas ------------------------------------------------------------
def _formula_html(name: str, equation: str, description: str | None) -> str:
    desc = f'<div class="ml-fdesc">{escape(description)}</div>' if description else ""
    return (f'<div class="ml-formula"><div class="ml-fname">{escape(name)}</div>'
            f'<div class="ml-feq">{escape(equation)}</div>{desc}</div>')


def formula_card(name: str, equation: str, description: str | None = None) -> None:
    """Render one centered formula card with a dark background."""
    st.markdown(f'<div class="ml-formula-grid">{_formula_html(name, equation, description)}</div>',
                unsafe_allow_html=True)


def formula_grid(formulas: list[tuple[str, str, str]]) -> None:
    """Render several formula cards in a responsive grid of (name, eq, desc)."""
    items = "".join(_formula_html(n, e, d) for n, e, d in formulas)
    st.markdown(f'<div class="ml-formula-grid">{items}</div>', unsafe_allow_html=True)


# --- Chips & callouts ----------------------------------------------------
def summary_chips(chips: list[tuple[str, str]]) -> None:
    """Render a row of "label: value" chips (e.g. current slider selections)."""
    items = "".join(f'<span class="ml-chip">{escape(l)} <b>{escape(v)}</b></span>'
                    for l, v in chips)
    st.markdown(f'<div class="ml-chips">{items}</div>', unsafe_allow_html=True)


def concept_chips(concepts: list[str]) -> None:
    """Render a row of plain concept chips."""
    items = "".join(f'<span class="ml-chip">{escape(c)}</span>' for c in concepts)
    st.markdown(f'<div class="ml-chips">{items}</div>', unsafe_allow_html=True)


_CALLOUTS = {
    "why": ("🎯", "Why this matters"),
    "intuition": ("💡", "Physical intuition"),
    "mistake": ("⚠️", "Common mistake"),
    "predict": ("🔮", "Predict before revealing"),
    "edge": ("🧪", "Edge case"),
    "info": ("ℹ️", "Good to know"),
}


def callout_card(body_html: str, kind: str = "info", title: str | None = None) -> None:
    """Render a titled, color-coded callout card.

    ``kind`` ∈ {why, intuition, mistake, predict, edge, info}. ``body_html`` may
    contain simple inline tags.
    """
    icon, default_title = _CALLOUTS.get(kind, _CALLOUTS["info"])
    head = escape(title) if title else default_title
    st.markdown(
        f'<div class="ml-callout ml-callout--{kind}">'
        f'<div class="ml-co-icon">{icon}</div>'
        f'<div><div class="ml-co-title">{head}</div>'
        f'<div class="ml-co-body">{body_html}</div></div></div>',
        unsafe_allow_html=True,
    )


# Older aliases.
callout = callout_card


def note(text_html: str) -> None:
    """Accented intuition callout (kept for older call sites)."""
    callout_card(text_html, kind="intuition")


# --- Stat cards ----------------------------------------------------------
def stat_card(label: str, value, sub: str | None = None, variant: str = "") -> str:
    """Return the HTML for a single gradient stat card."""
    sub_html = f'<div class="ml-stat-sub">{escape(sub)}</div>' if sub else ""
    return (f'<div class="ml-stat {variant}"><div class="ml-stat-label">{escape(label)}</div>'
            f'<div class="ml-stat-value">{escape(str(value))}</div>{sub_html}</div>')


def stat_cards(items: list[dict]) -> None:
    """Render a row of gradient stat cards.

    Each item dict accepts ``label``, ``value``, optional ``sub`` and ``variant``
    (``""``, ``alt``, ``warm``, ``cool``, ``slate``).
    """
    cards = "".join(stat_card(it["label"], it["value"], it.get("sub"),
                              it.get("variant", "")) for it in items)
    st.markdown(f'<div class="ml-stats">{cards}</div>', unsafe_allow_html=True)


# --- Tables --------------------------------------------------------------
def examples_table(headers: list[str], rows: list[list[str]],
                   mono_cols: tuple[int, ...] = ()) -> None:
    """Render a styled HTML table. ``mono_cols`` get the serif equation font."""
    head = "".join(f"<th>{escape(h)}</th>" for h in headers)
    body = ""
    for row in rows:
        cells = "".join(
            f'<td class="{"mono" if i in mono_cols else ""}">{escape(str(c))}</td>'
            for i, c in enumerate(row)
        )
        body += f"<tr>{cells}</tr>"
    st.markdown(f'<table class="ml-table"><thead><tr>{head}</tr></thead>'
                f'<tbody>{body}</tbody></table>', unsafe_allow_html=True)


# --- Plot framing --------------------------------------------------------
@contextmanager
def plot_shell(title: str, caption: str | None = None):
    """Context manager that frames a plot (or widgets) in a titled card.

    Usage::

        with ui.plot_shell("Orbit", "motion arrows and radius"):
            st.pyplot(fig)
    """
    box = st.container(border=True)
    with box:
        cap = f'<div class="ml-plot-cap">{escape(caption)}</div>' if caption else ""
        st.markdown(f'<div class="ml-plot-head"><div class="ml-plot-title">{escape(title)}</div>{cap}</div>',
                    unsafe_allow_html=True)
        yield box


# Older alias.
plot_card = plot_shell


@contextmanager
def control_panel(title: str | None = None, caption: str | None = None):
    """Context manager that frames interactive controls in a clean card."""
    box = st.container(border=True)
    with box:
        if title:
            cap = f'<div class="ml-plot-cap">{escape(caption)}</div>' if caption else ""
            st.markdown(f'<div class="ml-plot-head"><div class="ml-plot-title">{escape(title)}</div>{cap}</div>',
                        unsafe_allow_html=True)
        yield box


# --- Practice helpers ----------------------------------------------------
_DIFFICULTY_CLASS = {"Easy": "easy", "Medium": "medium", "Challenge": "challenge"}


@contextmanager
def practice_question_card(difficulty: str, topic: str, question: str,
                           qtype: str | None = None, mark: str = ""):
    """Frame a single practice question as a card and yield for the widgets.

    Renders the difficulty / topic badges and the question text, then yields a
    bordered container so the caller can add hint buttons and inputs.
    """
    box = st.container(border=True)
    with box:
        dcls = _DIFFICULTY_CLASS.get(difficulty, "muted")
        extra = (f'<span class="ml-pill muted">{escape(qtype)}</span>'
                 if qtype else "")
        st.markdown(
            f'<div class="ml-qhead"><div class="ml-qbadges">'
            f'<span class="ml-pill {dcls}">{escape(difficulty)}</span>'
            f'<span class="ml-pill topic">{escape(topic)}</span>{extra}</div>'
            f'<div class="ml-qtext">{escape(question)}{escape(mark)}</div></div>',
            unsafe_allow_html=True,
        )
        yield box


def hint_card(text: str, label: str = "Hint") -> None:
    """Render a custom hint card."""
    st.markdown(f'<div class="ml-hint"><b>{escape(label)}:</b> {escape(text)}</div>',
                unsafe_allow_html=True)


def result_card(correct: bool, body_html: str, concept: str | None = None) -> None:
    """Render the post-answer result/explanation card."""
    cls = "ok" if correct else "no"
    badge = "✅ Correct" if correct else "❌ Not quite"
    concept_html = (f'<span class="ml-concept">Related concept: {escape(concept)}</span>'
                    if concept else "")
    st.markdown(
        f'<div class="ml-result {cls}"><b>{badge}.</b> {body_html}{concept_html}</div>',
        unsafe_allow_html=True,
    )


def intuition_check(question: str, answer: str, key: str) -> None:
    """A lightweight 'predict, then reveal' check inside an expander."""
    with st.expander(f"🤔 Intuition check — {question}"):
        st.markdown(answer)


# --- Footer / CTA --------------------------------------------------------
def next_module_cta(label: str, target: str) -> None:
    """Render a primary button that navigates to the next module."""
    st.button(label, key=f"cta_{target}", type="primary",
              on_click=navigate_to, args=(target,))


def footer() -> None:
    """Render the app footer."""
    st.markdown(
        '<div class="ml-footer">'
        '<span class="ml-f-brand">🧲 Magnetism Lab</span>'
        '<span class="ml-f-meta">Built by Donny Nguyen · '
        '<a href="https://github.com/donnyphi" target="_blank">@donnyphi</a> · '
        'learn E&M by doing</span></div>',
        unsafe_allow_html=True,
    )
