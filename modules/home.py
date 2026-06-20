"""Landing page for Magnetism Lab."""
from __future__ import annotations

import streamlit as st

from utils import ui


def render() -> None:
    ui.hero(
        title="Magnetism Lab",
        subtitle="Interactive E&M simulations for right-hand rules, magnetic "
        "fields, and charged particle motion.",
        description="A freshman-friendly physics learning platform that turns "
        "magnetic field equations into interactive visual intuition.",
        pill="Learn E&M by doing",
    )

    # --- Module cards ----------------------------------------------------
    ui.section_header(
        "Explore the modules",
        "Four hands-on labs, each pairing a slider-driven simulation with "
        "plain-English explanations.",
    )
    ui.card_grid(
        [
            {"icon": "🖐️", "title": "Right-Hand Rule Trainer",
             "body": "Predict and check the direction of F = q(v × B) with a "
                     "labeled 3D vector plot.", "tag": "Direction intuition"},
            {"icon": "🧲", "title": "Magnetic Field Around a Wire",
             "body": "See circular field lines, dot/cross notation, and how B "
                     "falls off as 1/r.", "tag": "Fields"},
            {"icon": "🌀", "title": "Charged Particle Motion",
             "body": "Watch a charge curve in a uniform field and explore "
                     "radius, force, and period.", "tag": "Motion"},
            {"icon": "🎯", "title": "Practice Mode",
             "body": "20+ questions across five topics with hints, scoring, and "
                     "a personalized review.", "tag": "Mastery"},
        ]
    )

    # --- Learning path ---------------------------------------------------
    ui.section_header(
        "Your learning path",
        "Concepts build on each other — work through them in order.",
    )
    ui.learning_path(
        [
            ("Direction intuition", "Get comfortable with 3D directions and the "
             "right-hand rule before adding numbers."),
            ("Field from currents", "Learn how a current creates a circular "
             "magnetic field around a wire."),
            ("Force on moving charges", "Combine velocity and field to find the "
             "magnetic force via the cross product."),
            ("Particle motion", "See how that perpendicular force bends a charge "
             "into circular motion."),
            ("Practice and mastery", "Test yourself, track your streak, and find "
             "the topic to review next."),
        ]
    )

    # --- Why magnetism is confusing -------------------------------------
    ui.section_header(
        "Why magnetism feels confusing",
        "It's not just you — magnetism trips up almost every first-year student "
        "for a few specific reasons.",
    )
    ui.card_grid(
        [
            {"icon": "🧊", "title": "3D directions are hard",
             "body": "Velocity, field, and force all point in different "
                     "directions in space. Flat paper can't show that well."},
            {"icon": "✋", "title": "Cross products are unintuitive",
             "body": "v × B doesn't point along v or B — it points perpendicular "
                     "to both, which takes practice to picture."},
            {"icon": "➕", "title": "Charge sign flips everything",
             "body": "Swap a positive charge for a negative one and the force "
                     "reverses, even with the same v and B."},
            {"icon": "👻", "title": "Field lines are invisible",
             "body": "You can't see a magnetic field, so it's easy to lose track "
                     "of where it points and how strong it is."},
        ]
    )

    # --- Built for learning by doing ------------------------------------
    ui.section_header("Built for learning by doing")
    ui.note(
        "Every module follows the same rhythm: <b>learn the intuition</b>, "
        "<b>move the sliders</b> to see what changes, <b>predict</b> the answer "
        "before revealing it, and <b>check yourself</b> in practice. Active "
        "prediction beats passive reading — so the app nudges you to guess first."
    )

    # --- Concepts covered ------------------------------------------------
    ui.section_header("Concepts covered")
    concepts = [
        "Lorentz force", "Cross products", "Magnetic field around a wire",
        "Circular motion in magnetic fields", "Cyclotron period",
        "Charge sign and direction reversal",
    ]
    st.markdown(
        '<div class="ml-chips">'
        + "".join(f'<span class="ml-chip">{c}</span>' for c in concepts)
        + "</div>",
        unsafe_allow_html=True,
    )

    # --- How to use ------------------------------------------------------
    ui.section_header("How to use this app")
    ui.learning_path(
        [
            ("Learn the intuition", "Read the short explanation and formula "
             "cards at the top of each module."),
            ("Move the sliders", "Change the inputs and watch the plot and "
             "numbers respond in real time."),
            ("Predict before revealing", "Guess the answer first, then reveal it "
             "to test your mental model."),
            ("Check yourself with practice", "Head to Practice Mode to confirm "
             "the ideas stuck."),
        ]
    )

    st.caption("Use the sidebar to jump into any module. Start with the "
               "Right-Hand Rule Trainer if you're new to magnetism.")
