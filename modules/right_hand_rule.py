"""Right-Hand Rule Trainer module."""
from __future__ import annotations

import numpy as np
import streamlit as st

from utils import ui
from utils.physics import (
    DIRECTION_LABELS,
    direction_to_vector,
    is_zero_force,
    magnetic_force_direction,
)
from utils.plotting import plot_vectors

# Worked examples of the standard right-handed axis cross products.
_EXAMPLES = [
    ("+x × +y", "+z", "Standard right-handed order"),
    ("+y × +z", "+x", "Cycle x → y → z"),
    ("+z × +x", "+y", "Cycle continues"),
    ("+y × +x", "−z", "Swapping order flips the sign"),
]


def render() -> None:
    ui.page_hero(
        "🖐️", "Right-Hand Rule Trainer",
        "Find the direction of the magnetic force on a moving charge.",
    )
    ui.formula_card(
        "Magnetic force",
        "F = q (v × B)",
        "The force is the charge times the cross product of velocity and field.",
    )

    ui.steps_card("How to use your right hand", [
        "Point your fingers in the <b>velocity</b> direction.",
        "Curl them toward the <b>magnetic field</b> direction.",
        "Your thumb points along the <b>force</b> — for a positive charge.",
        "For a <b>negative</b> charge, reverse the thumb direction.",
    ])

    # --- Inputs ----------------------------------------------------------
    ui.section_header("Set up the scenario", eyebrow="Simulator")
    with ui.control_panel():
        c1, c2, c3 = st.columns(3)
        charge = c1.selectbox("Charge sign", ["positive", "negative"])
        v_dir = c2.selectbox("Velocity direction (v)", DIRECTION_LABELS, index=0)
        b_dir = c3.selectbox("Magnetic field direction (B)", DIRECTION_LABELS, index=2)
        ui.summary_chips([
            ("Charge", "+ q" if charge == "positive" else "− q"),
            ("Velocity", v_dir),
            ("Field", b_dir),
        ])

    f_dir = magnetic_force_direction(charge, v_dir, b_dir)
    zero = is_zero_force(v_dir, b_dir)

    # --- Predict-first mode ---------------------------------------------
    ui.section_header("Predict first, then reveal", eyebrow="Active recall")
    ui.callout_card(
        "Don't peek! Work out the force direction with your right hand, choose "
        "it below, then reveal the answer to check yourself.",
        kind="predict",
    )
    predict = st.toggle("Predict-first mode", value=True,
                        help="Guess the force direction before the app shows it.")

    guess = None
    if predict:
        options = DIRECTION_LABELS + ["zero (no force)"]
        guess = st.radio("Which way does the force point?", options,
                         horizontal=True, key="rhr_guess")

    if st.button("Reveal answer", type="primary"):
        _reveal(charge, v_dir, b_dir, f_dir, zero, guess if predict else None)

    # --- Vector plot -----------------------------------------------------
    f_vec = np.zeros(3) if zero else direction_to_vector(f_dir)
    with ui.plot_shell("3D vector view",
                       "Velocity (blue), magnetic field (green) and force (red)."):
        st.pyplot(plot_vectors(direction_to_vector(v_dir),
                               direction_to_vector(b_dir), f_vec, zero_force=zero))

    # --- Examples table --------------------------------------------------
    ui.section_header("Common cross-product examples", eyebrow="Reference")
    ui.examples_table(
        ["Expression", "Result", "Why"],
        [[e[0], e[1], e[2]] for e in _EXAMPLES],
        mono_cols=(0, 1),
    )

    ui.intuition_check(
        "Why is the force sometimes zero?",
        "Because F depends on **sin(θ)**, the angle between v and B. When v and "
        "B are **parallel or anti-parallel**, θ = 0° or 180°, so sin(θ) = 0 and "
        "the cross product — and therefore the force — vanishes.",
        key="rhr_zero",
    )

    ui.divider()
    ui.section_header("Next up")
    ui.next_module_cta("Continue to Field Around a Wire  →",
                       "🧲 Field Around a Wire")


def _reveal(charge, v_dir, b_dir, f_dir, zero, guess) -> None:
    """Show the answer and, in predict mode, whether the guess was right."""
    if zero:
        answer_label = "zero (no force)"
        ui.result_card(
            True,
            f"With v in <b>{v_dir}</b> and B in <b>{b_dir}</b>, the vectors are "
            "parallel or anti-parallel, so sin(θ) = 0 and F = q(v × B) = <b>0</b>.",
        )
    else:
        answer_label = f_dir
        ui.result_card(
            True,
            f"For a <b>{charge}</b> charge with <b>v = {v_dir}</b> and "
            f"<b>B = {b_dir}</b>, the force points in <b>{f_dir}</b>.",
        )

    if guess is not None:
        if guess == answer_label:
            st.balloons()
            ui.callout_card("Nice — your prediction was correct!", kind="why",
                            title="Prediction check")
        else:
            ui.callout_card(
                f"You picked <b>{guess}</b>, but the answer is "
                f"<b>{answer_label}</b>. Try the hand rule again.",
                kind="mistake", title="Prediction check",
            )
