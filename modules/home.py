"""Landing page for Magnetism Lab."""
from __future__ import annotations

from utils import ui


def render() -> None:
    ui.hero(
        title="Magnetism Lab",
        subtitle="Interactive E&M simulations for right-hand rules, magnetic "
        "fields, and charged particle motion.",
        description="A freshman-friendly physics learning platform that turns "
        "magnetic field equations into visual intuition.",
        badges=["Freshman E&M", "Vector Fields", "Lorentz Force",
                "Interactive Practice"],
    )

    # --- Module cards (clickable navigation) -----------------------------
    ui.section_header(
        "Explore the modules",
        "Four hands-on labs, each pairing a slider-driven simulation with "
        "plain-English explanations.",
        eyebrow="Start here",
    )
    ui.module_cards(
        [
            {"icon": "🖐️", "title": "Right-Hand Rule Trainer",
             "body": "Predict and check the direction of F = q(v × B) on a "
                     "labeled 3D vector plot.",
             "concepts": ["Cross products", "Force direction", "Charge sign"],
             "target": "🖐️ Right-Hand Rule"},
            {"icon": "🧲", "title": "Magnetic Field Around a Wire",
             "body": "See circular field lines, dot/cross notation, and how B "
                     "falls off as 1/r.",
             "concepts": ["Field lines", "⊙ / ⊗ notation", "1/r falloff"],
             "target": "🧲 Field Around a Wire"},
            {"icon": "🌀", "title": "Charged Particle Motion",
             "body": "Watch a charge curve in a uniform field and explore "
                     "radius, force, and period.",
             "concepts": ["Circular motion", "Cyclotron period", "Compare mode"],
             "target": "🌀 Charged Particle Motion"},
            {"icon": "🎯", "title": "Practice Mode",
             "body": "23 questions across five topics with hints, scoring, and "
                     "a personalized review.",
             "concepts": ["Hints", "Streaks", "Session summary"],
             "target": "🎯 Practice Mode"},
        ],
        columns=2,
    )

    ui.divider()

    # --- Learning path ---------------------------------------------------
    ui.section_header(
        "Your learning path",
        "Concepts build on each other — work through them in order.",
        eyebrow="Progression",
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

    ui.divider()

    # --- Why magnetism is confusing -------------------------------------
    ui.section_header(
        "Why magnetism feels confusing",
        "It's not just you — magnetism trips up almost every first-year student "
        "for a few specific reasons.",
        eyebrow="The challenge",
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

    ui.divider()

    # --- Built for learning by doing ------------------------------------
    ui.section_header("Built for learning by doing", eyebrow="The approach")
    ui.callout(
        "Every module follows the same rhythm: <b>learn the intuition</b>, "
        "<b>move the sliders</b> to see what changes, <b>predict</b> the answer "
        "before revealing it, and <b>check yourself</b> in practice. Active "
        "prediction beats passive reading — so the app nudges you to guess first.",
        kind="why",
    )

    # --- Concepts covered ------------------------------------------------
    ui.section_header("Concepts covered")
    ui.concept_chips([
        "Lorentz force", "Cross products", "Magnetic field around a wire",
        "Circular motion in magnetic fields", "Cyclotron period",
        "Charge sign and direction reversal",
    ])

    ui.divider()

    # --- How to use ------------------------------------------------------
    ui.section_header("How to use this app", eyebrow="Four steps")
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
