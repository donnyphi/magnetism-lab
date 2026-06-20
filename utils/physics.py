"""Core physics for Magnetism Lab.

Every magnetism formula used by the app lives here so the simulations and the
practice questions always agree on the math. Functions are kept small and pure
(no Streamlit, no plotting) so they are easy to unit test.
"""
from __future__ import annotations

import numpy as np

# Permeability of free space, μ₀ (T·m/A). Kept here as the single source of truth.
MU_0: float = 4 * np.pi * 1e-7

# Canonical unit vectors keyed by their human-readable label.
_DIRECTIONS: dict[str, np.ndarray] = {
    "+x": np.array([1.0, 0.0, 0.0]),
    "-x": np.array([-1.0, 0.0, 0.0]),
    "+y": np.array([0.0, 1.0, 0.0]),
    "-y": np.array([0.0, -1.0, 0.0]),
    "+z": np.array([0.0, 0.0, 1.0]),
    "-z": np.array([0.0, 0.0, -1.0]),
}

#: Direction labels in a stable order, handy for building UI dropdowns.
DIRECTION_LABELS: list[str] = ["+x", "-x", "+y", "-y", "+z", "-z"]


def direction_to_vector(direction: str) -> np.ndarray:
    """Return the unit vector for a label like ``"+x"`` or ``"-z"``.

    Raises:
        ValueError: if the label is not one of the six axis directions.
    """
    if direction not in _DIRECTIONS:
        raise ValueError(f"Unknown direction: {direction}")
    return _DIRECTIONS[direction].copy()


def vector_to_direction(vector: np.ndarray) -> str:
    """Collapse a vector to its dominant axis label, or ``"zero"``.

    Used to translate a cross-product result back into a friendly ``"+z"``-style
    answer. A (near) zero vector returns ``"zero"``.
    """
    vector = np.asarray(vector, dtype=float)
    if np.linalg.norm(vector) < 1e-12:
        return "zero"
    idx = int(np.argmax(np.abs(vector)))
    sign = "+" if vector[idx] > 0 else "-"
    axis = "xyz"[idx]
    return f"{sign}{axis}"


def magnetic_force_direction(
    charge_sign: str, velocity_direction: str, field_direction: str
) -> str:
    """Direction of ``F = q(v × B)`` as an axis label (or ``"zero"``).

    The cross product ``v × B`` gives the force direction for a *positive*
    charge. A negative charge flips it. When v and B are parallel or
    anti-parallel the cross product vanishes and the force is zero.

    Args:
        charge_sign: ``"positive"``/``"negative"`` (also accepts ``"+"``/``"-"``).
        velocity_direction: an axis label such as ``"+x"``.
        field_direction: an axis label such as ``"+y"``.

    Returns:
        An axis label like ``"+z"`` or the string ``"zero"``.
    """
    v = direction_to_vector(velocity_direction)
    b = direction_to_vector(field_direction)
    force = np.cross(v, b)
    if charge_sign.lower().startswith("neg") or charge_sign == "-":
        force = -force
    return vector_to_direction(force)


def is_zero_force(velocity_direction: str, field_direction: str) -> bool:
    """True when v ∥ B (parallel or anti-parallel), so sin(θ) = 0 and F = 0."""
    v = direction_to_vector(velocity_direction)
    b = direction_to_vector(field_direction)
    return bool(np.linalg.norm(np.cross(v, b)) < 1e-12)


def wire_field_strength(current: float, radius: float) -> float:
    """Magnetic field magnitude around a long straight wire: ``B = μ₀I / (2πr)``.

    Args:
        current: current ``I`` through the wire, in amperes.
        radius: perpendicular distance ``r`` from the wire, in metres (> 0).

    Returns:
        Field magnitude ``B`` in tesla.

    Raises:
        ValueError: if ``radius`` is not positive (the ideal formula diverges
            at the wire itself).
    """
    if radius <= 0:
        raise ValueError("radius must be positive")
    return MU_0 * current / (2 * np.pi * radius)


def charged_particle_radius(
    mass: float, speed: float, charge: float, magnetic_field: float
) -> float:
    """Radius of circular motion in a uniform field: ``r = mv / (|q|B)``.

    Args:
        mass: particle mass ``m`` in kg (> 0).
        speed: speed ``v`` in m/s (>= 0).
        charge: charge ``q`` in C (sign ignored; magnitude must be non-zero).
        magnetic_field: field ``B`` in tesla (> 0).

    Raises:
        ValueError: if any argument is outside its physical range. With ``q = 0``
            or ``B = 0`` there is no magnetic force and the orbit is undefined.
    """
    if mass <= 0 or speed < 0 or charge == 0 or magnetic_field <= 0:
        raise ValueError(
            "mass > 0, speed >= 0, charge != 0, and magnetic_field > 0 are required"
        )
    return mass * speed / (abs(charge) * magnetic_field)


def magnetic_force_magnitude(
    charge: float, speed: float, magnetic_field: float, angle_deg: float = 90.0
) -> float:
    """Magnitude of the magnetic force: ``F = |q| v B sin(θ)``.

    Args:
        charge: charge ``q`` in C (only the magnitude matters).
        speed: speed ``v`` in m/s.
        magnetic_field: field ``B`` in tesla.
        angle_deg: angle between v and B in degrees. Defaults to 90° (the
            perpendicular case that gives the maximum force).

    Returns:
        Force magnitude in newtons. Returns 0 when ``q``, ``v``, ``B`` or
        ``sin(θ)`` is zero.
    """
    return abs(charge) * speed * magnetic_field * abs(np.sin(np.radians(angle_deg)))


def cyclotron_period(mass: float, charge: float, magnetic_field: float) -> float:
    """Time for one full orbit: ``T = 2πm / (|q|B)``.

    Notably independent of speed and radius. Raises ``ValueError`` for
    ``mass <= 0``, ``charge == 0`` or ``magnetic_field <= 0``.
    """
    if mass <= 0 or charge == 0 or magnetic_field <= 0:
        raise ValueError("mass > 0, charge != 0, and magnetic_field > 0 are required")
    return 2 * np.pi * mass / (abs(charge) * magnetic_field)


def cyclotron_frequency(mass: float, charge: float, magnetic_field: float) -> float:
    """Angular frequency of the orbit: ``ω = |q|B / m`` (radians per second)."""
    if mass <= 0 or charge == 0 or magnetic_field <= 0:
        raise ValueError("mass > 0, charge != 0, and magnetic_field > 0 are required")
    return abs(charge) * magnetic_field / mass
