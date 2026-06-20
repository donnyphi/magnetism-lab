"""Charged Particle Motion module."""
from __future__ import annotations

import streamlit as st

from utils import ui
from utils.physics import (
    charged_particle_radius,
    cyclotron_frequency,
    cyclotron_period,
    magnetic_force_magnitude,
)
from utils.plotting import plot_orbit_comparison, plot_particle_circle


def render() -> None:
    ui.page_hero(
        "🌀", "Charged Particle Motion",
        "A charge moving across a uniform magnetic field travels in a circle.",
        theme="teal",
    )

    ui.callout_card(
        "The magnetic force is <b>always perpendicular to the velocity</b>. A "
        "perpendicular force can't speed the particle up or slow it down — it "
        "only <b>changes its direction</b>. Constantly turning at a fixed speed "
        "is exactly what circular motion is.",
        kind="intuition",
    )

    ui.formula_grid([
        ("Force", "F = |q| v B", "Magnetic force magnitude."),
        ("Radius", "r = m v / (|q| B)", "Size of the circle."),
        ("Period", "T = 2π m / (|q| B)", "Time for one full loop."),
        ("Angular frequency", "ω = |q| B / m", "How fast it sweeps around."),
    ])

    # --- Inputs ----------------------------------------------------------
    ui.section_header("Set the particle", eyebrow="Simulator")
    with ui.control_panel():
        c1, c2, c3 = st.columns(3)
        charge_sign = c1.selectbox("Charge sign", ["positive", "negative"])
        q_mag = c1.slider("Charge magnitude |q| (C)", 0.1, 5.0, 1.0)
        mass = c2.slider("Mass m (kg)", 0.1, 10.0, 1.0)
        speed = c2.slider("Speed v (m/s)", 0.1, 20.0, 5.0)
        B = c3.slider("Magnetic field B (T)", 0.1, 10.0, 2.0)
        q = q_mag if charge_sign == "positive" else -q_mag
        ui.summary_chips([
            ("Charge", f"{'+' if charge_sign == 'positive' else '−'}{q_mag:.1f} C"),
            ("Mass", f"{mass:.1f} kg"),
            ("Speed", f"{speed:.1f} m/s"),
            ("Field", f"{B:.1f} T"),
        ])

    # --- Outputs ---------------------------------------------------------
    r = charged_particle_radius(mass, speed, q, B)
    F = magnetic_force_magnitude(q, speed, B)
    T = cyclotron_period(mass, q, B)
    omega = cyclotron_frequency(mass, q, B)

    ui.section_header("Results", eyebrow="Calculated")
    ui.stat_cards([
        {"label": "Radius r", "value": f"{r:.3f} m"},
        {"label": "Force F", "value": f"{F:.3f} N", "variant": "warm"},
        {"label": "Period T", "value": f"{T:.3f} s", "variant": "alt"},
        {"label": "Angular freq ω", "value": f"{omega:.3f}", "sub": "rad/s",
         "variant": "cool"},
    ])

    with ui.plot_shell("Orbit",
                       "Motion arrow, center and radius line for the circular path."):
        st.pyplot(plot_particle_circle(r, charge_sign))

    # --- Compare mode ----------------------------------------------------
    ui.section_header("Compare mode", eyebrow="What changes?",
                      subtitle="Change one quantity and see how the orbit responds.")
    with ui.control_panel():
        change = st.radio(
            "Compare current settings with…",
            ["Doubled B", "Halved B", "Doubled mass", "Doubled speed"],
            horizontal=True, key="cp_compare",
        )
    r2, label2 = _compare_radius(change, mass, speed, q, B)
    ratio = r2 / r if r else float("nan")
    ui.stat_cards([
        {"label": "Original radius", "value": f"{r:.3f} m", "variant": "slate"},
        {"label": "New radius", "value": f"{r2:.3f} m",
         "sub": f"{ratio:.2f}× the original", "variant": "warm"},
    ])
    with ui.plot_shell("Orbit comparison",
                       "Solid = current settings, dashed = changed setting."):
        st.pyplot(plot_orbit_comparison(r, r2, "current", label2, charge_sign))

    # --- Intuition cards -------------------------------------------------
    ui.section_header("Intuition", eyebrow="Rules of thumb")
    ui.card_grid([
        {"icon": "🔽", "title": "Stronger B → tighter circle",
         "body": "B is in the denominator of r = mv/(|q|B), so more field bends "
                 "the path more sharply."},
        {"icon": "🚀", "title": "Faster v → larger circle",
         "body": "Speed is in the numerator, so a faster particle sweeps out a "
                 "larger radius."},
        {"icon": "⚖️", "title": "Larger m → larger circle",
         "body": "Heavier particles have more inertia and are harder to turn, so "
                 "the circle grows."},
        {"icon": "🔄", "title": "Negative charge → opposite curve",
         "body": "Flipping the sign of the charge flips the force, so the "
                 "particle curves the other way (same radius)."},
    ])

    ui.intuition_check(
        "What if B = 0, q = 0, or v = 0?",
        "All three switch off the magnetic force F = |q|vB:\n\n"
        "- **B = 0** — no field, no magnetic force, so the particle goes "
        "straight (no circle).\n"
        "- **q = 0** — a neutral particle feels no magnetic force at all.\n"
        "- **v = 0** — a charge at rest feels no magnetic force; it only kicks "
        "in once the charge is moving.",
        key="cp_edge",
    )

    ui.divider()
    ui.section_header("Next up")
    ui.next_module_cta("Test yourself in Practice Mode  →", "🎯 Practice Mode")


def _compare_radius(change: str, mass, speed, q, B):
    """Return ``(new_radius, label)`` for the selected single-variable change."""
    if change == "Doubled B":
        return charged_particle_radius(mass, speed, q, B * 2), "B × 2"
    if change == "Halved B":
        return charged_particle_radius(mass, speed, q, B / 2), "B ÷ 2"
    if change == "Doubled mass":
        return charged_particle_radius(mass * 2, speed, q, B), "m × 2"
    return charged_particle_radius(mass, speed * 2, q, B), "v × 2"
