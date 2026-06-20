"""Reusable UI building blocks for Magnetism Lab.

Streamlit's default widgets are functional but plain. This module keeps all of
the custom HTML/CSS in one place so the page modules stay readable: instead of
pasting long ``st.markdown(...)`` strings everywhere, they call small helpers
like :func:`hero`, :func:`module_cards`, :func:`formula_card` and
:func:`callout`.

The stylesheet is split into a few named chunks (base, components, widgets) and
joined once in :func:`inject_global_styles`, so no single unreadable HTML blob
lives anywhere.
"""
from __future__ import annotations

from contextlib import contextmanager
from html import escape

import streamlit as st

# --- Design tokens -------------------------------------------------------
# A small, consistent palette keeps the whole app feeling like one product.
INK = "#0f172a"        # near-black slate for headings
BODY = "#475569"       # muted slate for body copy
MUTED = "#64748b"
PRIMARY = "#4f46e5"    # indigo
PRIMARY_DK = "#4338ca"
PRIMARY_SOFT = "#eef2ff"
ACCENT = "#7c3aed"     # violet
LINE = "#e7eaf3"
SURFACE = "#ffffff"

# Semantic colors for callouts / feedback.
OK = "#0f9d58"
WARN = "#d97706"
DANGER = "#dc2626"
INFO = "#2563eb"

# --- CSS, in maintainable chunks -----------------------------------------
_CSS_BASE = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Fraunces:opsz,wght@9..144,500;600;700&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

/* Subtle, app-like background gradient instead of flat white. */
.stApp {{
    background:
        radial-gradient(1200px 600px at 12% -8%, #eef2ff 0%, rgba(238,242,255,0) 55%),
        radial-gradient(1000px 520px at 110% 0%, #f5f0ff 0%, rgba(245,240,255,0) 50%),
        linear-gradient(180deg, #fbfcff 0%, #f6f8fd 100%);
}}
[data-testid="stHeader"] {{ background: transparent; }}

.block-container {{ padding-top: 2.0rem; padding-bottom: 4rem; max-width: 1080px; }}

h1, h2, h3, h4 {{ color: {INK}; letter-spacing: -0.01em; }}

/* Clean section divider. */
.ml-divider {{
    height: 1px; border: 0; margin: 2rem 0 1.4rem;
    background: linear-gradient(90deg, rgba(79,70,229,.0), {LINE} 18%, {LINE} 82%, rgba(79,70,229,.0));
}}
"""

_CSS_COMPONENTS = f"""
/* Hero ---------------------------------------------------------------- */
.ml-hero {{
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #9333ea 100%);
    border-radius: 26px; padding: 3rem 2.6rem; color: #fff;
    box-shadow: 0 24px 60px -24px rgba(79,70,229,0.65);
    margin-bottom: 1.4rem;
}}
.ml-hero::after {{
    content: ""; position: absolute; right: -90px; top: -90px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle at center, rgba(255,255,255,.20), rgba(255,255,255,0) 70%);
}}
.ml-hero h1 {{ font-size: 3rem; font-weight: 800; margin: 0 0 .5rem; color:#fff; line-height: 1.05; }}
.ml-hero .ml-sub {{ font-size: 1.18rem; font-weight: 600; opacity: .96; margin-bottom: .7rem; max-width: 720px; }}
.ml-hero .ml-desc {{ font-size: 1.02rem; opacity: .88; max-width: 640px; line-height: 1.6; }}
.ml-badges {{ display:flex; flex-wrap:wrap; gap:.5rem; margin-top: 1.3rem; }}
.ml-badge {{
    display:inline-flex; align-items:center; gap:.35rem;
    background: rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.34);
    border-radius: 999px; padding:.34rem .85rem; font-size:.82rem; font-weight:600;
    backdrop-filter: blur(4px);
}}

/* Section headers ----------------------------------------------------- */
.ml-section {{ margin: 1.9rem 0 .9rem; }}
.ml-eyebrow {{
    display:inline-block; text-transform:uppercase; letter-spacing:.12em;
    font-size:.72rem; font-weight:700; color:{PRIMARY};
    background:{PRIMARY_SOFT}; padding:.2rem .6rem; border-radius:7px; margin-bottom:.5rem;
}}
.ml-section h2 {{ font-size: 1.6rem; font-weight: 800; margin:0; }}
.ml-section p {{ color: {BODY}; margin:.3rem 0 0; font-size: 1rem; max-width: 760px; }}

/* Generic + module cards --------------------------------------------- */
.ml-grid {{ display:grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); }}
.ml-grid-2 {{ display:grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
.ml-card {{
    background: {SURFACE}; border: 1px solid {LINE}; border-radius: 18px;
    padding: 1.3rem 1.35rem; box-shadow: 0 10px 26px -20px rgba(15,23,42,0.35);
    transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
    height: 100%;
}}
.ml-card:hover {{ transform: translateY(-4px); box-shadow: 0 22px 38px -22px rgba(79,70,229,0.5); border-color:#d7d9ee; }}
.ml-card .ml-icon {{
    display:inline-flex; align-items:center; justify-content:center;
    width:46px; height:46px; border-radius:13px; font-size:1.55rem;
    background: {PRIMARY_SOFT};
}}
.ml-card h3 {{ font-size: 1.12rem; font-weight: 700; margin: .65rem 0 .35rem; }}
.ml-card p {{ color:{BODY}; font-size: .93rem; line-height: 1.55; margin:0; }}
.ml-card .ml-tag {{
    display:inline-block; background:{PRIMARY_SOFT}; color:{PRIMARY};
    border-radius:8px; padding:.14rem .55rem; font-size:.72rem; font-weight:700; margin-top:.7rem;
}}
.ml-card .ml-concepts {{ display:flex; flex-wrap:wrap; gap:.35rem; margin-top:.8rem; }}
.ml-card .ml-concepts span {{
    font-size:.72rem; font-weight:600; color:{MUTED};
    border:1px solid {LINE}; border-radius:7px; padding:.12rem .5rem;
}}

/* Numbered learning-path steps --------------------------------------- */
.ml-step {{ display:flex; gap:.95rem; align-items:flex-start; margin-bottom:.9rem; }}
.ml-step .ml-num {{
    flex:0 0 auto; width:36px; height:36px; border-radius:11px;
    background: linear-gradient(135deg, {PRIMARY}, {ACCENT}); color:#fff; font-weight:800;
    display:flex; align-items:center; justify-content:center; font-size:.95rem;
    box-shadow: 0 8px 16px -8px rgba(79,70,229,.6);
}}
.ml-step .ml-step-body h4 {{ margin:0; font-size:1.02rem; font-weight:700; }}
.ml-step .ml-step-body p {{ margin:.12rem 0 0; color:{BODY}; font-size:.92rem; }}

/* Formula cards ------------------------------------------------------- */
.ml-formula-grid {{ display:grid; gap: .8rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin-bottom:.4rem; }}
.ml-formula {{
    background: linear-gradient(160deg, #111827 0%, #1e1b4b 100%);
    border: 1px solid rgba(124,58,237,.35); border-radius: 16px;
    padding: 1.1rem 1.25rem; color: #e2e8f0; text-align:center;
    box-shadow: 0 14px 30px -22px rgba(30,27,75,.9);
}}
.ml-formula .ml-fname {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.1em; color:#a5b4fc; font-weight:700; }}
.ml-formula .ml-feq {{
    font-family: 'Fraunces', Georgia, serif; font-size: 1.7rem; font-weight: 600;
    color:#fff; margin:.4rem 0; letter-spacing:.01em;
}}
.ml-formula .ml-fdesc {{ font-size:.84rem; color:#c7d2fe; line-height:1.45; }}

/* Chips --------------------------------------------------------------- */
.ml-chips {{ display:flex; flex-wrap:wrap; gap:.5rem; margin:.5rem 0 .9rem; }}
.ml-chip {{
    background:#fff; color:{PRIMARY}; border:1px solid {LINE}; border-radius:10px;
    padding:.38rem .8rem; font-size:.86rem; font-weight:600;
}}
.ml-chip b {{ color:{INK}; }}

/* Callouts ------------------------------------------------------------ */
.ml-callout {{
    display:flex; gap:.85rem; align-items:flex-start;
    border:1px solid {LINE}; border-left-width:5px; border-radius:14px;
    padding: .95rem 1.1rem; margin:.5rem 0 1rem; background:#fff;
    box-shadow: 0 8px 22px -20px rgba(15,23,42,.4);
}}
.ml-callout .ml-co-icon {{ font-size:1.3rem; line-height:1.4; }}
.ml-callout .ml-co-title {{ font-weight:700; color:{INK}; font-size:.95rem; margin-bottom:.15rem; }}
.ml-callout .ml-co-body {{ color:{BODY}; font-size:.93rem; line-height:1.55; }}
.ml-callout .ml-co-body b {{ color:{INK}; }}

/* Practice badges & stat cards --------------------------------------- */
.ml-qbadges {{ display:flex; flex-wrap:wrap; gap:.45rem; margin-bottom:.7rem; }}
.ml-pill {{ display:inline-block; border-radius:999px; padding:.2rem .65rem; font-size:.74rem; font-weight:700; }}
.ml-stats {{ display:grid; gap:.8rem; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); margin:.3rem 0 1rem; }}
.ml-stat {{
    border-radius:16px; padding:1rem 1.1rem; color:#fff;
    background: linear-gradient(135deg, {PRIMARY}, {ACCENT});
    box-shadow: 0 14px 30px -20px rgba(79,70,229,.7);
}}
.ml-stat .ml-stat-label {{ font-size:.76rem; text-transform:uppercase; letter-spacing:.08em; opacity:.9; font-weight:700; }}
.ml-stat .ml-stat-value {{ font-size:1.9rem; font-weight:800; line-height:1.15; margin-top:.2rem; }}
.ml-stat .ml-stat-sub {{ font-size:.78rem; opacity:.88; margin-top:.1rem; }}
.ml-stat.alt {{ background: linear-gradient(135deg, #0ea5e9, #6366f1); }}
.ml-stat.warm {{ background: linear-gradient(135deg, #f59e0b, #ef4444); }}
.ml-stat.cool {{ background: linear-gradient(135deg, #10b981, #0ea5e9); }}

/* Plot title inside bordered containers ------------------------------ */
.ml-plot-title {{ font-weight:700; font-size:1.02rem; color:{INK}; margin-bottom:.1rem; }}
.ml-plot-cap {{ color:{MUTED}; font-size:.86rem; margin-bottom:.4rem; }}
"""

_CSS_WIDGETS = f"""
/* Buttons ------------------------------------------------------------- */
.stButton > button {{
    border-radius: 11px; font-weight: 600; border: 1px solid {LINE};
    padding: .5rem 1rem; transition: all .15s ease; background:#fff; color:{INK};
}}
.stButton > button:hover {{ border-color:{PRIMARY}; color:{PRIMARY}; transform: translateY(-1px); }}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {PRIMARY}, {ACCENT}); color:#fff; border:0;
    box-shadow: 0 12px 24px -14px rgba(79,70,229,.8);
}}
.stButton > button[kind="primary"]:hover {{ filter: brightness(1.06); color:#fff; }}

/* Metrics as soft cards ---------------------------------------------- */
[data-testid="stMetric"] {{
    background:#fff; border:1px solid {LINE}; border-radius:14px;
    padding: .85rem 1rem; box-shadow: 0 8px 20px -18px rgba(15,23,42,.4);
}}
[data-testid="stMetricValue"] {{ font-weight:800; color:{INK}; }}
[data-testid="stMetricLabel"] {{ color:{MUTED}; font-weight:600; }}

/* Bordered containers (used to frame plots) -------------------------- */
[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius:18px !important; border-color:{LINE} !important;
    background:#fff; box-shadow: 0 12px 30px -24px rgba(15,23,42,.45);
}}

/* Expanders as cards -------------------------------------------------- */
[data-testid="stExpander"] {{
    border:1px solid {LINE} !important; border-radius:14px !important;
    background:#fff; box-shadow: 0 8px 22px -20px rgba(15,23,42,.4); overflow:hidden;
    margin-bottom:.6rem;
}}
[data-testid="stExpander"] summary {{ font-weight:600; }}
[data-testid="stExpander"] summary:hover {{ color:{PRIMARY}; }}

/* Sidebar ------------------------------------------------------------- */
[data-testid="stSidebar"] {{ background: linear-gradient(180deg, #ffffff, #f4f6fd); border-right:1px solid {LINE}; }}

/* Tighten radio / selectbox spacing a touch. */
[data-testid="stRadio"] label {{ font-weight:500; }}

/* Responsive ---------------------------------------------------------- */
@media (max-width: 640px) {{
    .ml-hero {{ padding: 2rem 1.4rem; border-radius:20px; }}
    .ml-hero h1 {{ font-size: 2.1rem; }}
    .ml-hero .ml-sub {{ font-size: 1.02rem; }}
    .block-container {{ padding-left: .8rem; padding-right: .8rem; }}
}}
"""


def inject_global_styles() -> None:
    """Inject the app-wide stylesheet once. Safe to call on every render."""
    css = f"<style>{_CSS_BASE}{_CSS_COMPONENTS}{_CSS_WIDGETS}</style>"
    st.markdown(css, unsafe_allow_html=True)


# Backwards-compatible alias (older call sites use this name).
inject_global_css = inject_global_styles


# --- Navigation ----------------------------------------------------------
def navigate_to(page: str) -> None:
    """Set the active page (used by module-card CTA buttons via ``on_click``)."""
    st.session_state["page"] = page


# --- Layout helpers ------------------------------------------------------
def hero(title: str, subtitle: str, description: str,
         badges: list[str] | None = None) -> None:
    """Render the gradient landing hero with title, subtitle, blurb and badges."""
    badge_html = ""
    if badges:
        chips = "".join(f'<span class="ml-badge">✦ {escape(b)}</span>' for b in badges)
        badge_html = f'<div class="ml-badges">{chips}</div>'
    st.markdown(
        f"""
        <div class="ml-hero">
            <h1>{escape(title)}</h1>
            <div class="ml-sub">{escape(subtitle)}</div>
            <div class="ml-desc">{escape(description)}</div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str | None = None,
                   eyebrow: str | None = None) -> None:
    """Render a styled section heading with an optional eyebrow and subtitle."""
    eb = f'<span class="ml-eyebrow">{escape(eyebrow)}</span><br>' if eyebrow else ""
    sub = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f'<div class="ml-section">{eb}<h2>{escape(title)}</h2>{sub}</div>',
        unsafe_allow_html=True,
    )


def divider() -> None:
    """Render a soft, centered section divider."""
    st.markdown('<hr class="ml-divider">', unsafe_allow_html=True)


# --- Cards ---------------------------------------------------------------
def _card_html(icon: str, title: str, body: str,
               tag: str | None = None, concepts: list[str] | None = None) -> str:
    tag_html = f'<span class="ml-tag">{escape(tag)}</span>' if tag else ""
    icon_html = f'<div class="ml-icon">{escape(icon)}</div>' if icon else ""
    concepts_html = ""
    if concepts:
        pills = "".join(f"<span>{escape(c)}</span>" for c in concepts)
        concepts_html = f'<div class="ml-concepts">{pills}</div>'
    return (
        f'<div class="ml-card">{icon_html}'
        f'<h3>{escape(title)}</h3><p>{escape(body)}</p>{tag_html}{concepts_html}</div>'
    )


def card_grid(cards: list[dict], wide: bool = False) -> None:
    """Render a responsive grid of static cards.

    Each card dict accepts ``icon``, ``title``, ``body``, optional ``tag`` and
    an optional ``concepts`` list of short labels.
    """
    cls = "ml-grid-2" if wide else "ml-grid"
    items = "".join(
        _card_html(c.get("icon", ""), c["title"], c["body"],
                   c.get("tag"), c.get("concepts"))
        for c in cards
    )
    st.markdown(f'<div class="{cls}">{items}</div>', unsafe_allow_html=True)


def module_cards(cards: list[dict], columns: int = 2) -> None:
    """Render large module cards, each with a real navigation CTA button.

    Each card dict needs ``icon``, ``title``, ``body``, ``target`` (the page
    label to navigate to) and an optional ``concepts`` list. Cards are laid out
    in ``columns`` Streamlit columns (which stack on narrow screens).
    """
    for row_start in range(0, len(cards), columns):
        row = cards[row_start:row_start + columns]
        cols = st.columns(len(row), gap="medium")
        for col, c in zip(cols, row):
            with col:
                st.markdown(
                    _card_html(c.get("icon", ""), c["title"], c["body"],
                               concepts=c.get("concepts")),
                    unsafe_allow_html=True,
                )
                st.button(
                    "Start module  →",
                    key=f"nav_{c['target']}", type="primary",
                    use_container_width=True,
                    on_click=navigate_to, args=(c["target"],),
                )


def learning_path(steps: list[tuple[str, str]]) -> None:
    """Render a numbered, vertical progression of (title, description) steps."""
    rows = "".join(
        f'<div class="ml-step"><div class="ml-num">{i}</div>'
        f'<div class="ml-step-body"><h4>{escape(t)}</h4><p>{escape(d)}</p></div></div>'
        for i, (t, d) in enumerate(steps, start=1)
    )
    st.markdown(rows, unsafe_allow_html=True)


# --- Formulas ------------------------------------------------------------
def _formula_html(name: str, equation: str, description: str | None) -> str:
    desc = f'<div class="ml-fdesc">{escape(description)}</div>' if description else ""
    return (
        f'<div class="ml-formula"><div class="ml-fname">{escape(name)}</div>'
        f'<div class="ml-feq">{escape(equation)}</div>{desc}</div>'
    )


def formula_card(name: str, equation: str, description: str | None = None) -> None:
    """Render a single centered formula card."""
    st.markdown(_formula_html(name, equation, description), unsafe_allow_html=True)


def formula_grid(formulas: list[tuple[str, str, str]]) -> None:
    """Render several formula cards in a responsive grid.

    ``formulas`` is a list of ``(name, equation, description)`` tuples.
    """
    items = "".join(_formula_html(n, e, d) for n, e, d in formulas)
    st.markdown(f'<div class="ml-formula-grid">{items}</div>', unsafe_allow_html=True)


# --- Chips & callouts ----------------------------------------------------
def summary_chips(chips: list[tuple[str, str]]) -> None:
    """Render a row of "label: value" chips, e.g. the current slider selections."""
    items = "".join(
        f'<span class="ml-chip">{escape(label)} <b>{escape(value)}</b></span>'
        for label, value in chips
    )
    st.markdown(f'<div class="ml-chips">{items}</div>', unsafe_allow_html=True)


def concept_chips(concepts: list[str]) -> None:
    """Render a row of plain concept chips."""
    items = "".join(f'<span class="ml-chip">{escape(c)}</span>' for c in concepts)
    st.markdown(f'<div class="ml-chips">{items}</div>', unsafe_allow_html=True)


# Callout presets: kind -> (icon, default title, accent color).
_CALLOUTS = {
    "why": ("🎯", "Why this matters", PRIMARY),
    "intuition": ("💡", "Physical intuition", ACCENT),
    "mistake": ("⚠️", "Common mistake", DANGER),
    "predict": ("🔮", "Predict before revealing", INFO),
    "edge": ("🧪", "Edge case", MUTED),
    "info": ("ℹ️", "Good to know", INFO),
}


def callout(body_html: str, kind: str = "info", title: str | None = None) -> None:
    """Render a titled, color-coded callout box.

    ``kind`` is one of ``why``, ``intuition``, ``mistake``, ``predict``,
    ``edge`` or ``info``. ``body_html`` may contain simple inline tags.
    """
    icon, default_title, color = _CALLOUTS.get(kind, _CALLOUTS["info"])
    head = escape(title) if title else default_title
    st.markdown(
        f'<div class="ml-callout" style="border-left-color:{color}">'
        f'<div class="ml-co-icon">{icon}</div>'
        f'<div><div class="ml-co-title">{head}</div>'
        f'<div class="ml-co-body">{body_html}</div></div></div>',
        unsafe_allow_html=True,
    )


def note(text_html: str) -> None:
    """Accented intuition callout (kept for older call sites)."""
    callout(text_html, kind="intuition")


# --- Plot framing --------------------------------------------------------
@contextmanager
def plot_card(title: str, caption: str | None = None):
    """Context manager that frames a plot (or any widgets) in a titled card.

    Usage::

        with ui.plot_card("Vector view", "v, B and F drawn to scale"):
            st.pyplot(fig)
    """
    box = st.container(border=True)
    with box:
        st.markdown(f'<div class="ml-plot-title">{escape(title)}</div>',
                    unsafe_allow_html=True)
        if caption:
            st.markdown(f'<div class="ml-plot-cap">{escape(caption)}</div>',
                        unsafe_allow_html=True)
        yield box


# --- Practice helpers ----------------------------------------------------
_DIFFICULTY_STYLE = {
    "Easy": ("#dcfce7", "#15803d"),
    "Medium": ("#fef3c7", "#b45309"),
    "Challenge": ("#fee2e2", "#b91c1c"),
}


def difficulty_pill(level: str) -> str:
    """Return HTML for a colored difficulty pill."""
    bg, fg = _DIFFICULTY_STYLE.get(level, (PRIMARY_SOFT, PRIMARY))
    return f'<span class="ml-pill" style="background:{bg};color:{fg}">{escape(level)}</span>'


def topic_pill(topic: str) -> str:
    """Return HTML for a neutral topic pill."""
    return (f'<span class="ml-pill" style="background:{PRIMARY_SOFT};'
            f'color:{PRIMARY}">{escape(topic)}</span>')


def question_badges(difficulty: str, topic: str, extra: str | None = None) -> None:
    """Render the difficulty + topic pills row shown inside a question card."""
    extra_html = (f'<span class="ml-pill" style="background:#f1f5f9;color:{MUTED}">'
                  f'{escape(extra)}</span>') if extra else ""
    st.markdown(
        f'<div class="ml-qbadges">{difficulty_pill(difficulty)}'
        f'{topic_pill(topic)}{extra_html}</div>',
        unsafe_allow_html=True,
    )


def stat_cards(items: list[dict]) -> None:
    """Render a row of gradient stat cards.

    Each item dict accepts ``label``, ``value``, optional ``sub`` and optional
    ``variant`` (``""``, ``alt``, ``warm``, ``cool``).
    """
    cards = ""
    for it in items:
        variant = it.get("variant", "")
        sub = f'<div class="ml-stat-sub">{escape(it["sub"])}</div>' if it.get("sub") else ""
        cards += (
            f'<div class="ml-stat {variant}">'
            f'<div class="ml-stat-label">{escape(it["label"])}</div>'
            f'<div class="ml-stat-value">{escape(str(it["value"]))}</div>{sub}</div>'
        )
    st.markdown(f'<div class="ml-stats">{cards}</div>', unsafe_allow_html=True)


def intuition_check(question: str, answer: str, key: str) -> None:
    """A lightweight 'predict, then reveal' check inside an expander."""
    with st.expander(f"🤔 Intuition check — {question}"):
        st.markdown(answer)
