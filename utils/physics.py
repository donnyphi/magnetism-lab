"""Physics helpers for Magnetism Lab.

The functions in this module keep the Streamlit UI focused on explanation while
centralizing the vector math and freshman-level E&M formulas in one testable
place.
"""

from __future__ import annotations

import numpy as np

MU_0 = 4 * np.pi * 1e-7

_DIRECTION_VECTORS = {
    "+x": np.array([1.0, 0.0, 0.0]),
    "-x": np.array([-1.0, 0.0, 0.0]),
    "+y": np.array([0.0, 1.0, 0.0]),
    "-y": np.array([0.0, -1.0, 0.0]),
    "+z": np.array([0.0, 0.0, 1.0]),
    "-z": np.array([0.0, 0.0, -1.0]),
}


def direction_to_vector(direction: str) -> np.ndarray:
    """Convert a direction label such as '+x' into a Cartesian unit vector."""
    try:
        return _DIRECTION_VECTORS[direction].copy()
    except KeyError as exc:
        valid = ", ".join(_DIRECTION_VECTORS)
        raise ValueError(f"Unknown direction '{direction}'. Choose one of: {valid}") from exc


def vector_to_direction(vector: np.ndarray) -> str:
    """Convert an axis-aligned vector into a direction label, or 'zero'."""
    vector = np.asarray(vector, dtype=float)
    if np.allclose(vector, np.zeros(3)):
        return "zero"

    dominant_axis = int(np.argmax(np.abs(vector)))
    sign = "+" if vector[dominant_axis] > 0 else "-"
    axis = ("x", "y", "z")[dominant_axis]
    return f"{sign}{axis}"


def magnetic_force_direction(
    charge_sign: str, velocity_direction: str, field_direction: str
) -> str:
    """Return the direction of q(v x B) for axis-aligned velocity and field."""
    velocity = direction_to_vector(velocity_direction)
    magnetic_field = direction_to_vector(field_direction)
    force = np.cross(velocity, magnetic_field)

    if charge_sign.lower() in {"negative", "-", "negative charge"}:
        force = -force
    elif charge_sign.lower() not in {"positive", "+", "positive charge"}:
        raise ValueError("charge_sign must be 'positive' or 'negative'.")

    return vector_to_direction(force)


def wire_field_strength(current: float, radius: float) -> float:
    """Magnetic field strength around a long straight wire: B = mu0 I / 2 pi r."""
    if radius <= 0:
        raise ValueError("radius must be positive.")
    return MU_0 * abs(current) / (2 * np.pi * radius)


def charged_particle_radius(
    mass: float, speed: float, charge: float, magnetic_field: float
) -> float:
    """Radius for circular motion when velocity is perpendicular to B."""
    if mass <= 0:
        raise ValueError("mass must be positive.")
    if speed < 0:
        raise ValueError("speed cannot be negative.")
    if charge == 0:
        raise ValueError("charge cannot be zero.")
    if magnetic_field <= 0:
        raise ValueError("magnetic_field must be positive.")
    return mass * speed / (abs(charge) * magnetic_field)


def magnetic_force_magnitude(charge: float, speed: float, magnetic_field: float) -> float:
    """Magnitude of magnetic force for perpendicular velocity and field."""
    if speed < 0:
        raise ValueError("speed cannot be negative.")
    if magnetic_field < 0:
        raise ValueError("magnetic_field cannot be negative.")
    return abs(charge) * speed * magnetic_field


def cyclotron_period(mass: float, charge: float, magnetic_field: float) -> float:
    """Circular motion period T = 2 pi m / |q|B."""
    if mass <= 0:
        raise ValueError("mass must be positive.")
    if charge == 0:
        raise ValueError("charge cannot be zero.")
    if magnetic_field <= 0:
        raise ValueError("magnetic_field must be positive.")
    return 2 * np.pi * mass / (abs(charge) * magnetic_field)
