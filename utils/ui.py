"""Reusable UI building blocks for Magnetism Lab.

Streamlit's default widgets are functional but plain. This module keeps all of
the custom HTML/CSS in one place so the page modules stay readable: instead of
pasting long ``st.markdown(...)`` strings everywhere, they call small helpers
like :func:`hero`, :func:`card` and :func:`formula_card`.
"""
from __future__ import annotations

from html import escape

import streamlit as st

# --- Design tokens -------------------------------------------------------
# A small, consistent palette keeps the whole app feeling like one product.
INK = "#0f172a"        # near-black slate for headings
BODY = "#475569"       # muted slate for body copy
PRIMARY = "#4f46e5"    # indigo
PRIMARY_SOFT = "#eef2ff"
ACCENT = "#7c3aed"     # violet
SURFACE = "#ffffff"
LINE = "#e2e8f0"

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

/* Tame Streamlit's default top padding for a tighter, app-like feel. */
.block-container {{ padding-top: 2.2rem; max-width: 1100px; }}

/* Hero ---------------------------------------------------------------- */
.ml-hero {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {ACCENT} 100%);
    border-radius: 22px;
    padding: 2.6rem 2.4rem;
    color: #fff;
    box-shadow: 0 18px 40px -18px rgba(79,70,229,0.55);
    margin-bottom: 1.6rem;
}}
.ml-hero h1 {{ font-size: 2.5rem; font-weight: 800; margin: 0 0 .4rem 0; color:#fff; }}
.ml-hero .ml-sub {{ font-size: 1.12rem; font-weight: 600; opacity: .95; margin-bottom: .6rem; }}
.ml-hero .ml-desc {{ font-size: 1rem; opacity: .9; max-width: 640px; line-height: 1.55; }}
.ml-hero .ml-pill {{
    display:inline-block; background: rgba(255,255,255,.18);
    border:1px solid rgba(255,255,255,.35); border-radius: 999px;
    padding: .25rem .8rem; font-size:.8rem; font-weight:600; margin-bottom: 1rem;
}}

/* Section headers ----------------------------------------------------- */
.ml-section {{ margin: 1.8rem 0 .8rem 0; }}
.ml-section h2 {{ font-size: 1.5rem; font-weight: 700; color: {INK}; margin:0; }}
.ml-section p {{ color: {BODY}; margin: .25rem 0 0 0; font-size: .98rem; }}

/* Cards --------------------------------------------------------------- */
.ml-grid {{ display:grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
.ml-grid-2 {{ display:grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
.ml-card {{
    background: {SURFACE};
    border: 1px solid {LINE};
    border-radius: 16px;
    padding: 1.2rem 1.25rem;
    box-shadow: 0 8px 22px -16px rgba(15,23,42,0.25);
    transition: transform .15s ease, box-shadow .15s ease;
    height: 100%;
}}
.ml-card:hover {{ transform: translateY(-3px); box-shadow: 0 16px 30px -18px rgba(79,70,229,0.45); }}
.ml-card .ml-icon {{ font-size: 1.7rem; }}
.ml-card h3 {{ font-size: 1.08rem; font-weight: 700; color:{INK}; margin: .5rem 0 .3rem 0; }}
.ml-card p {{ color:{BODY}; font-size: .92rem; line-height: 1.5; margin:0; }}
.ml-card .ml-tag {{
    display:inline-block; background:{PRIMARY_SOFT}; color:{PRIMARY};
    border-radius:8px; padding:.12rem .5rem; font-size:.72rem; font-weight:600; margin-top:.6rem;
}}

/* Numbered learning-path steps --------------------------------------- */
.ml-step {{ display:flex; gap: .9rem; align-items:flex-start; margin-bottom: .85rem; }}
.ml-step .ml-num {{
    flex: 0 0 auto; width: 34px; height: 34px; border-radius: 10px;
    background: {PRIMARY}; color:#fff; font-weight:700; display:flex;
    align-items:center; justify-content:center; font-size: .95rem;
}}
.ml-step .ml-step-body h4 {{ margin:0; font-size:1rem; color:{INK}; font-weight:600; }}
.ml-step .ml-step-body p {{ margin:.1rem 0 0 0; color:{BODY}; font-size:.9rem; }}

/* Formula cards ------------------------------------------------------- */
.ml-formula {{
    background: {INK};
    border-radius: 14px;
    padding: 1rem 1.2rem;
    color: #e2e8f0;
    margin-bottom: .7rem;
}}
.ml-formula .ml-fname {{ font-size:.78rem; text-transform:uppercase; letter-spacing:.06em; color:#a5b4fc; font-weight:600; }}
.ml-formula .ml-feq {{ font-size: 1.4rem; font-weight: 700; color:#fff; margin:.25rem 0; font-family:'Inter',serif; }}
.ml-formula .ml-fdesc {{ font-size:.85rem; color:#cbd5e1; }}

/* Summary chips ------------------------------------------------------- */
.ml-chips {{ display:flex; flex-wrap:wrap; gap:.5rem; margin:.4rem 0 .8rem 0; }}
.ml-chip {{
    background:{PRIMARY_SOFT}; color:{PRIMARY}; border-radius:10px;
    padding:.35rem .75rem; font-size:.85rem; font-weight:600;
}}
.ml-chip b {{ color:{INK}; }}

/* Callout ------------------------------------------------------------- */
.ml-note {{
    border-left: 4px solid {ACCENT};
    background: #faf5ff;
    border-radius: 0 12px 12px 0;
    padding: .8rem 1rem; color:{BODY}; font-size:.92rem; line-height:1.5;
}}
.ml-note b {{ color:{INK}; }}
</style>
"""


def inject_global_css() -> None:
    """Inject the app-wide stylesheet. Safe to call once per page render."""
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str, description: str, pill: str | None = None) -> None:
    """Render the gradient landing hero with title, subtitle and blurb."""
    pill_html = f'<span class="ml-pill">{escape(pill)}</span>' if pill else ""
    st.markdown(
        f"""
        <div class="ml-hero">
            {pill_html}
            <h1>{escape(title)}</h1>
            <div class="ml-sub">{escape(subtitle)}</div>
            <div class="ml-desc">{escape(description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str | None = None) -> None:
    """Render a styled section heading with an optional one-line subtitle."""
    sub = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f'<div class="ml-section"><h2>{escape(title)}</h2>{sub}</div>',
        unsafe_allow_html=True,
    )


def _card_html(icon: str, title: str, body: str, tag: str | None = None) -> str:
    tag_html = f'<span class="ml-tag">{escape(tag)}</span>' if tag else ""
    icon_html = f'<div class="ml-icon">{escape(icon)}</div>' if icon else ""
    return (
        f'<div class="ml-card">{icon_html}'
        f'<h3>{escape(title)}</h3><p>{escape(body)}</p>{tag_html}</div>'
    )


def card_grid(cards: list[dict], wide: bool = False) -> None:
    """Render a responsive grid of cards.

    Each card dict accepts ``icon``, ``title``, ``body`` and optional ``tag``.
    """
    cls = "ml-grid-2" if wide else "ml-grid"
    items = "".join(
        _card_html(c.get("icon", ""), c["title"], c["body"], c.get("tag"))
        for c in cards
    )
    st.markdown(f'<div class="{cls}">{items}</div>', unsafe_allow_html=True)


def learning_path(steps: list[tuple[str, str]]) -> None:
    """Render a numbered, vertical progression of (title, description) steps."""
    rows = "".join(
        f'<div class="ml-step"><div class="ml-num">{i}</div>'
        f'<div class="ml-step-body"><h4>{escape(t)}</h4><p>{escape(d)}</p></div></div>'
        for i, (t, d) in enumerate(steps, start=1)
    )
    st.markdown(rows, unsafe_allow_html=True)


def formula_card(name: str, equation: str, description: str) -> None:
    """Render a dark formula card: a label, the equation, and a plain-words note."""
    st.markdown(
        f'<div class="ml-formula"><div class="ml-fname">{escape(name)}</div>'
        f'<div class="ml-feq">{escape(equation)}</div>'
        f'<div class="ml-fdesc">{escape(description)}</div></div>',
        unsafe_allow_html=True,
    )


def summary_chips(chips: list[tuple[str, str]]) -> None:
    """Render a row of "label: value" chips, e.g. the current slider selections."""
    items = "".join(
        f'<span class="ml-chip">{escape(label)} <b>{escape(value)}</b></span>'
        for label, value in chips
    )
    st.markdown(f'<div class="ml-chips">{items}</div>', unsafe_allow_html=True)


def note(text_html: str) -> None:
    """Render an accented callout. ``text_html`` may contain simple inline tags."""
    st.markdown(f'<div class="ml-note">{text_html}</div>', unsafe_allow_html=True)


def intuition_check(question: str, answer: str, key: str) -> None:
    """A lightweight 'predict, then reveal' check inside an expander."""
    with st.expander(f"🤔 Intuition check — {question}"):
        st.markdown(answer)
