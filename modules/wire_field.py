"""Magnetic Field Around a Wire module."""
from __future__ import annotations

import streamlit as st

from utils import ui
from utils.physics import wire_field_strength
from utils.plotting import plot_field_vs_distance, plot_wire_field


def render() -> None:
    ui.section_header(
        "Magnetic Field Around a Wire",
        "A long straight current makes circular magnetic field lines.",
    )
    ui.formula_card(
        "Field around a long straight wire",
        "B = μ₀ I / (2π r)",
        "Field strength grows with current I and shrinks with distance r.",
    )

    ui.callout(
        "Dot / cross notation shows 3D direction on flat paper:<br>"
        "⊙ a <b>dot</b> is an arrow tip coming <b>toward you</b> (current out of "
        "the page).<br>"
        "⊗ a <b>cross</b> is an arrow tail going <b>away from you</b> (current "
        "into the page).",
        kind="intuition", title="Reading dot / cross notation",
    )

    # --- Inputs ----------------------------------------------------------
    ui.section_header("Set up the wire")
    c1, c2 = st.columns(2)
    current = c1.slider("Current I (A)", 0.1, 20.0, 5.0)
    radius = c2.slider("Distance r from wire (m)", 0.01, 5.0, 1.0)
    direction = st.radio("Current direction", ["out of page", "into page"],
                         horizontal=True)

    circulation = "counter-clockwise" if direction == "out of page" else "clockwise"
    ui.summary_chips([
        ("Current", f"{current:.1f} A"),
        ("Distance", f"{radius:.2f} m"),
        ("Direction", "⊙ out of page" if direction == "out of page" else "⊗ into page"),
        ("Field circulates", circulation),
    ])

    B = wire_field_strength(current, radius)
    st.metric("Magnetic field strength B", f"{B * 1e6:.3f} µT", help=f"{B:.3e} T")

    with ui.plot_card("Field lines around the wire",
                      "Arrows show the circulation direction of B."):
        st.pyplot(plot_wire_field(direction))

    # --- Distance scaling mini-experiment --------------------------------
    ui.section_header(
        "Distance scaling experiment",
        "Keep the current fixed and watch B shrink as you move away.",
    )
    cols = st.columns(3)
    for col, factor in zip(cols, (1, 2, 3)):
        b_here = wire_field_strength(current, radius * factor)
        label = "B at r" if factor == 1 else f"B at {factor}r"
        col.metric(label, f"{b_here * 1e6:.3f} µT")
    ui.callout(
        "Because <b>B ∝ 1/r</b>, doubling the distance <b>halves</b> the field "
        "and tripling it cuts the field to <b>one third</b>. It's a steady "
        "falloff, not a sudden cutoff.",
        kind="why",
    )
    with ui.plot_card("B versus distance",
                      "The 1/r curve with r, 2r and 3r marked."):
        st.pyplot(plot_field_vs_distance(current))

    # --- Interactive question -------------------------------------------
    ui.section_header("Quick check")
    answer = st.radio(
        "If the distance from the wire doubles, what happens to the magnetic field?",
        ["It doubles", "It halves", "It stays the same", "It quadruples"],
        index=None, key="wire_q",
    )
    if answer:
        if answer == "It halves":
            st.success("✅ Correct! B ∝ 1/r, so doubling r halves B.")
        else:
            st.error("❌ Not quite. Since B = μ₀I/(2πr), doubling r halves B.")

    # --- Edge case -------------------------------------------------------
    ui.intuition_check(
        "What happens right at the wire (r → 0)?",
        "The formula **B = μ₀I/(2πr)** blows up to infinity as r → 0, which is "
        "why distance can't be zero. In reality a wire has a finite thickness, "
        "and **inside** the wire the field actually grows *linearly* from zero at "
        "the center. The ideal formula only applies **outside** the wire.",
        key="wire_edge",
    )
