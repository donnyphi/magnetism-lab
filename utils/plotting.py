"""Matplotlib figures for Magnetism Lab.

The figures aim to be *legible first*: consistent colors, clear axis labels, and
direction arrows so a first-year student can read intuition straight off the
plot. All helpers return a Matplotlib ``Figure`` for ``st.pyplot``.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

# Shared palette so v / B / F mean the same color everywhere in the app.
COLOR_V = "#2563eb"  # velocity  – blue
COLOR_B = "#16a34a"  # field     – green
COLOR_F = "#dc2626"  # force     – red
COLOR_ACCENT = "#7c3aed"  # violet accent
COLOR_MUTED = "#94a3b8"
COLOR_COMPARE = "#f59e0b"  # amber, for "compare" overlays


def plot_vectors(v, b, f, *, zero_force: bool = False):
    """3D quiver of velocity, magnetic field and force from the right-hand rule.

    Vectors are drawn as fixed-length unit arrows (only direction matters here)
    and color-coded to match the rest of the app. When ``zero_force`` is set the
    F arrow is omitted and a banner is shown instead.
    """
    fig = plt.figure(figsize=(6, 5.2))
    ax = fig.add_subplot(111, projection="3d")

    arrows = [(v, "v (velocity)", COLOR_V), (b, "B (field)", COLOR_B)]
    if not zero_force:
        arrows.append((f, "F (force)", COLOR_F))

    for vec, label, color in arrows:
        vec = np.asarray(vec, dtype=float)
        if np.linalg.norm(vec) > 1e-12:
            ax.quiver(
                0, 0, 0, vec[0], vec[1], vec[2],
                length=1.0, normalize=True, color=color, linewidth=2.6,
                arrow_length_ratio=0.18,
            )
            ax.text(vec[0] * 1.15, vec[1] * 1.15, vec[2] * 1.15, label,
                    color=color, fontsize=10, fontweight="bold")

    # Faint reference axes through the origin.
    for axis in (([-1, 1], [0, 0], [0, 0]), ([0, 0], [-1, 1], [0, 0]),
                 ([0, 0], [0, 0], [-1, 1])):
        ax.plot(*axis, color=COLOR_MUTED, linewidth=0.6, alpha=0.6)

    ax.set_xlim([-1, 1]); ax.set_ylim([-1, 1]); ax.set_zlim([-1, 1])
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    title = "Force is zero (v ∥ B)" if zero_force else "Right-hand rule: v × B"
    ax.set_title(title, fontsize=12, fontweight="bold")
    fig.tight_layout()
    return fig


def plot_wire_field(current_direction: str):
    """Circular field lines around a wire, with ⊙ / ⊗ for current direction.

    ``current_direction`` is ``"out of page"`` (counter-clockwise field) or
    ``"into page"`` (clockwise field).
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    out_of_page = current_direction == "out of page"
    sign = 1 if out_of_page else -1

    # Concentric field-line circles with a direction arrow on each.
    for r in (0.6, 1.1, 1.6):
        theta = np.linspace(0, 2 * np.pi, 200)
        ax.plot(r * np.cos(theta), r * np.sin(theta),
                color=COLOR_ACCENT, linewidth=1.4, alpha=0.8)
        # Arrowhead showing circulation direction at the top of each circle.
        ax.annotate(
            "", xy=(sign * 0.12, r), xytext=(0, r),
            arrowprops=dict(arrowstyle="-|>", color=COLOR_ACCENT, lw=1.6),
        )

    # The wire itself: ⊙ out of page, ⊗ into page.
    ax.scatter([0], [0], s=900, facecolors="white",
               edgecolors=COLOR_F, linewidths=2.2, zorder=5)
    ax.text(0, 0, "•" if out_of_page else "×",
            ha="center", va="center", fontsize=24 if out_of_page else 20,
            color=COLOR_F, fontweight="bold", zorder=6)

    circulation = "counter-clockwise" if out_of_page else "clockwise"
    symbol = "⊙ out of page" if out_of_page else "⊗ into page"
    ax.set_title(f"Current {symbol}  →  field is {circulation}",
                 fontsize=12, fontweight="bold")
    ax.set_xlim([-2, 2]); ax.set_ylim([-2, 2])
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    ax.grid(True, alpha=0.15)
    fig.tight_layout()
    return fig


def plot_particle_circle(radius: float, charge_sign: str):
    """Orbit of a charged particle, with motion arrows, center and radius line."""
    fig, ax = plt.subplots(figsize=(6, 6))
    _draw_orbit(ax, radius, charge_sign, color=COLOR_V, label="path")

    ax.set_title("Circular motion in a uniform magnetic field",
                 fontsize=12, fontweight="bold")
    lim = radius * 1.35 + 1e-9
    ax.set_xlim([-lim, lim]); ax.set_ylim([-lim, lim])
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    ax.grid(True, alpha=0.15)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    return fig


def plot_orbit_comparison(radius_a: float, radius_b: float,
                          label_a: str, label_b: str, charge_sign: str):
    """Overlay two orbits (e.g. current settings vs. doubled B) for comparison."""
    fig, ax = plt.subplots(figsize=(6, 6))
    _draw_orbit(ax, radius_a, charge_sign, color=COLOR_V, label=label_a, center=False)
    _draw_orbit(ax, radius_b, charge_sign, color=COLOR_COMPARE, label=label_b,
                center=False, dashed=True)
    ax.scatter([0], [0], color="black", s=40, zorder=6)

    ax.set_title("Comparing two orbits", fontsize=12, fontweight="bold")
    lim = max(radius_a, radius_b) * 1.35 + 1e-9
    ax.set_xlim([-lim, lim]); ax.set_ylim([-lim, lim])
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    ax.grid(True, alpha=0.15)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    return fig


def plot_field_vs_distance(current: float, max_radius: float = 3.0):
    """Show the 1/r falloff of ``B`` and mark B at r, 2r, 3r."""
    from utils.physics import wire_field_strength

    r = np.linspace(0.2, max_radius, 200)
    b = np.array([wire_field_strength(current, ri) for ri in r])

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(r, b * 1e6, color=COLOR_ACCENT, linewidth=2.2)

    for ri, marker in ((1.0, "r"), (2.0, "2r"), (3.0, "3r")):
        if ri <= max_radius:
            bi = wire_field_strength(current, ri) * 1e6
            ax.scatter([ri], [bi], color=COLOR_F, zorder=5)
            ax.annotate(marker, (ri, bi), textcoords="offset points",
                        xytext=(6, 8), fontsize=10, fontweight="bold")

    ax.set_title("Field strength falls off as 1/r", fontsize=12, fontweight="bold")
    ax.set_xlabel("distance r (m)"); ax.set_ylabel("B (µT)")
    ax.grid(True, alpha=0.2)
    fig.tight_layout()
    return fig


def _draw_orbit(ax, radius, charge_sign, *, color, label, center=True, dashed=False):
    """Draw one orbit circle with a motion arrow, center dot and radius line."""
    theta = np.linspace(0, 2 * np.pi, 500)
    # Positive and negative charges circulate in opposite senses.
    direction = -1 if charge_sign == "positive" else 1
    x = radius * np.cos(direction * theta)
    y = radius * np.sin(direction * theta)

    ax.plot(x, y, color=color, linewidth=2.2,
            linestyle="--" if dashed else "-",
            label=f"{label} (r = {radius:.2f} m)")

    # Radius line from center to the starting point.
    ax.plot([0, x[0]], [0, y[0]], color=color, linewidth=1.0, alpha=0.6)
    ax.scatter([x[0]], [y[0]], color=color, s=55, zorder=6)

    # Motion-direction arrow a quarter turn along the path.
    i = len(theta) // 12
    ax.annotate("", xy=(x[i], y[i]), xytext=(x[0], y[0]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2))

    if center:
        ax.scatter([0], [0], color="black", s=45, zorder=6, label="center")
