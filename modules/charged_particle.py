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
    ui.section_header(
        "Charged Particle Motion",
        "A charge moving across a uniform magnetic field travels in a circle.",
    )

    ui.note(
        "The magnetic force is <b>always perpendicular to the velocity</b>. A "
        "perpendicular force can't speed the particle up or slow it down — it "
        "only <b>changes its direction</b>. Constantly turning at a fixed speed "
        "is exactly what circular motion is."
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        ui.formula_card("Force", "F = |q| v B", "Magnetic force magnitude.")
    with col_b:
        ui.formula_card("Radius", "r = m v / (|q| B)", "Size of the circle.")
    with col_c:
        ui.formula_card("Period", "T = 2π m / (|q| B)", "Time for one full loop.")

    # --- Inputs ----------------------------------------------------------
    ui.section_header("Set the particle")
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

    ui.section_header("Results")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Radius r", f"{r:.3f} m")
    m2.metric("Force F", f"{F:.3f} N")
    m3.metric("Period T", f"{T:.3f} s")
    m4.metric("Angular freq. ω", f"{omega:.3f} rad/s")

    st.pyplot(plot_particle_circle(r, charge_sign))

    # --- Compare mode ----------------------------------------------------
    ui.section_header(
        "Compare mode",
        "Change one quantity and see how the orbit responds.",
    )
    change = st.radio(
        "Compare current settings with…",
        ["Doubled B", "Halved B", "Doubled mass", "Doubled speed"],
        horizontal=True, key="cp_compare",
    )
    r2, label2 = _compare_radius(change, mass, speed, q, B)
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        st.metric("New radius", f"{r2:.3f} m", delta=f"{r2 - r:+.3f} m")
        ratio = r2 / r if r else float("nan")
        st.caption(f"That's **{ratio:.2f}×** the original radius.")
    with cc2:
        st.pyplot(plot_orbit_comparison(r, r2, "current", label2, charge_sign))

    # --- Intuition cards -------------------------------------------------
    ui.section_header("Intuition")
    ui.card_grid([
        {"icon": "🔽", "title": "Stronger B → tighter circle",
         "body": "B is in the denominator of r = mv/(|q|B), so more field bends "
                 "the path more sharply."},
        {"icon": "🚀", "title": "Faster v → bigger circle",
         "body": "Speed is in the numerator, so a faster particle sweeps out a "
                 "larger radius."},
        {"icon": "⚖️", "title": "Larger m → bigger circle",
         "body": "Heavier particles have more inertia and are harder to turn, so "
                 "the circle grows."},
        {"icon": "⚡", "title": "Larger |q| → tighter circle",
         "body": "More charge means a stronger force for the same field, bending "
                 "the path more tightly."},
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


def _compare_radius(change: str, mass, speed, q, B):
    """Return ``(new_radius, label)`` for the selected single-variable change."""
    if change == "Doubled B":
        return charged_particle_radius(mass, speed, q, B * 2), "B × 2"
    if change == "Halved B":
        return charged_particle_radius(mass, speed, q, B / 2), "B ÷ 2"
    if change == "Doubled mass":
        return charged_particle_radius(mass * 2, speed, q, B), "m × 2"
    return charged_particle_radius(mass, speed * 2, q, B), "v × 2"
