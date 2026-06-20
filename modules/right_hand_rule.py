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
    ("+x × +y", "+z"),
    ("+y × +z", "+x"),
    ("+z × +x", "+y"),
    ("+y × +x", "-z  (swapping order flips the sign)"),
]


def render() -> None:
    ui.section_header(
        "Right-Hand Rule Trainer",
        "Find the direction of the magnetic force on a moving charge.",
    )
    ui.formula_card(
        "Magnetic force",
        "F = q (v × B)",
        "The force is the charge times the cross product of velocity and field.",
    )

    ui.note(
        "<b>How to do it with your hand:</b><br>"
        "1. Point your fingers in the <b>velocity</b> direction.<br>"
        "2. Curl them toward the <b>magnetic field</b> direction.<br>"
        "3. Your thumb points along the <b>force</b> — for a positive charge.<br>"
        "4. For a <b>negative</b> charge, reverse the thumb direction."
    )

    # --- Inputs ----------------------------------------------------------
    ui.section_header("Set up the scenario")
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
    ui.section_header("Predict first, then reveal")
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
    st.pyplot(plot_vectors(direction_to_vector(v_dir),
                           direction_to_vector(b_dir), f_vec, zero_force=zero))

    # --- Examples table --------------------------------------------------
    ui.section_header("Common cross-product examples")
    st.table({"Expression": [e[0] for e in _EXAMPLES],
              "Result": [e[1] for e in _EXAMPLES]})

    ui.intuition_check(
        "Why is the force sometimes zero?",
        "Because F depends on **sin(θ)**, the angle between v and B. When v and "
        "B are **parallel or anti-parallel**, θ = 0° or 180°, so sin(θ) = 0 and "
        "the cross product — and therefore the force — vanishes.",
        key="rhr_zero",
    )


def _reveal(charge, v_dir, b_dir, f_dir, zero, guess) -> None:
    """Show the answer and, in predict mode, whether the guess was right."""
    if zero:
        answer_label = "zero (no force)"
        st.success(
            f"**Force is zero.** With v in {v_dir} and B in {b_dir}, the vectors "
            "are parallel or anti-parallel, so sin(θ) = 0 and F = q(v × B) = 0."
        )
    else:
        answer_label = f_dir
        st.success(
            f"For a **{charge}** charge with **v = {v_dir}** and **B = {b_dir}**, "
            f"the force points in **{f_dir}**."
        )

    if guess is not None:
        if guess == answer_label:
            st.balloons()
            st.info("✅ Nice — your prediction was correct!")
        else:
            st.warning(f"❌ You picked **{guess}**, but the answer is "
                       f"**{answer_label}**. Try the hand rule again.")
