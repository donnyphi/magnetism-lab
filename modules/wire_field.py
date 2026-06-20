"""Magnetic Field Around a Wire module."""
from __future__ import annotations

import streamlit as st

from utils import ui
from utils.physics import wire_field_strength
from utils.plotting import plot_field_vs_distance, plot_wire_field


def render() -> None:
    ui.page_hero(
        "🧲", "Magnetic Field Around a Wire",
        "A long straight current makes circular magnetic field lines.",
        theme="green",
    )
    ui.formula_card(
        "Field around a long straight wire",
        "B = μ₀ I / (2π r)",
        "Field strength grows with current I and shrinks with distance r.",
    )

    # --- Dot / cross notation -------------------------------------------
    ui.section_header("Reading dot / cross notation", eyebrow="3D on flat paper")
    ui.card_grid([
        {"icon": "⊙", "title": "Dot — out of the page",
         "body": "A dot is the tip of an arrow flying toward you. The current "
                 "comes out of the page; the field circulates counter-clockwise."},
        {"icon": "⊗", "title": "Cross — into the page",
         "body": "A cross is the tail of an arrow flying away. The current goes "
                 "into the page; the field circulates clockwise."},
    ], wide=True)

    # --- Inputs ----------------------------------------------------------
    ui.section_header("Set up the wire", eyebrow="Simulator")
    with ui.control_panel():
        c1, c2 = st.columns(2)
        current = c1.slider("Current I (A)", 0.1, 20.0, 5.0)
        radius = c2.slider("Distance r from wire (m)", 0.01, 5.0, 1.0)
        direction = st.radio("Current direction", ["out of page", "into page"],
                             horizontal=True)
        circulation = ("counter-clockwise" if direction == "out of page"
                       else "clockwise")
        ui.summary_chips([
            ("Current", f"{current:.1f} A"),
            ("Distance", f"{radius:.2f} m"),
            ("Direction",
             "⊙ out of page" if direction == "out of page" else "⊗ into page"),
            ("Circulates", circulation),
        ])

    B = wire_field_strength(current, radius)
    ui.stat_cards([
        {"label": "Field strength B", "value": f"{B * 1e6:.3f} µT",
         "sub": f"{B:.2e} T at r = {radius:.2f} m"},
    ])

    with ui.plot_shell("Field lines around the wire",
                       "Arrows show the circulation direction of B."):
        st.pyplot(plot_wire_field(direction))

    # --- Distance scaling experiment ------------------------------------
    ui.section_header("Distance scaling experiment", eyebrow="The 1/r law",
                      subtitle="Keep the current fixed and watch B shrink as you "
                      "move away.")
    ui.stat_cards([
        {"label": "B at r", "value": f"{wire_field_strength(current, radius) * 1e6:.2f} µT",
         "variant": "cool"},
        {"label": "B at 2r", "value": f"{wire_field_strength(current, radius * 2) * 1e6:.2f} µT",
         "variant": "alt"},
        {"label": "B at 3r", "value": f"{wire_field_strength(current, radius * 3) * 1e6:.2f} µT",
         "variant": "slate"},
    ])
    ui.callout_card(
        "Because <b>B ∝ 1/r</b>, doubling the distance <b>halves</b> the field "
        "and tripling it cuts the field to <b>one third</b>. It's a steady "
        "falloff, not a sudden cutoff.",
        kind="why",
    )
    with ui.plot_shell("B versus distance",
                       "The 1/r curve with r, 2r and 3r marked."):
        st.pyplot(plot_field_vs_distance(current))

    # --- Quick check -----------------------------------------------------
    ui.section_header("Quick check", eyebrow="Test yourself")
    answer = st.radio(
        "If the distance from the wire doubles, what happens to the magnetic field?",
        ["It doubles", "It halves", "It stays the same", "It quadruples"],
        index=None, key="wire_q",
    )
    if answer == "It halves":
        ui.result_card(True, "B ∝ 1/r, so doubling r halves B.")
    elif answer is not None:
        ui.result_card(False, "Since B = μ₀I/(2πr), doubling r <b>halves</b> B.")

    # --- Edge case -------------------------------------------------------
    ui.callout_card(
        "The formula <b>B = μ₀I/(2πr)</b> blows up to infinity as r → 0, which "
        "is why distance can't be zero. A real wire has finite thickness, and "
        "<b>inside</b> the wire the field grows linearly from zero at the center. "
        "The ideal formula only applies <b>outside</b> the wire.",
        kind="edge", title="Edge case: r → 0",
    )

    ui.divider()
    ui.section_header("Next up")
    ui.next_module_cta("Continue to Charged Particle Motion  →",
                       "🌀 Charged Particle Motion")
