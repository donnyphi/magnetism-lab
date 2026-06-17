"""Physics helpers for Magnetism Lab."""
from __future__ import annotations
import numpy as np

MU_0 = 4 * np.pi * 1e-7

_DIRECTIONS = {
    "+x": np.array([1.0, 0.0, 0.0]),
    "-x": np.array([-1.0, 0.0, 0.0]),
    "+y": np.array([0.0, 1.0, 0.0]),
    "-y": np.array([0.0, -1.0, 0.0]),
    "+z": np.array([0.0, 0.0, 1.0]),
    "-z": np.array([0.0, 0.0, -1.0]),
}

def direction_to_vector(direction: str) -> np.ndarray:
    if direction not in _DIRECTIONS:
        raise ValueError(f"Unknown direction: {direction}")
    return _DIRECTIONS[direction].copy()

def vector_to_direction(vector: np.ndarray) -> str:
    vector = np.asarray(vector, dtype=float)
    if np.linalg.norm(vector) < 1e-12:
        return "zero"
    idx = int(np.argmax(np.abs(vector)))
    sign = "+" if vector[idx] > 0 else "-"
    axis = "xyz"[idx]
    return f"{sign}{axis}"

def magnetic_force_direction(charge_sign: str, velocity_direction: str, field_direction: str) -> str:
    v = direction_to_vector(velocity_direction)
    b = direction_to_vector(field_direction)
    force = np.cross(v, b)
    if charge_sign.lower().startswith("neg") or charge_sign == "-":
        force = -force
    return vector_to_direction(force)

def wire_field_strength(current: float, radius: float) -> float:
    if radius <= 0:
        raise ValueError("radius must be positive")
    return MU_0 * current / (2 * np.pi * radius)

def charged_particle_radius(mass: float, speed: float, charge: float, magnetic_field: float) -> float:
    if mass <= 0 or speed < 0 or charge == 0 or magnetic_field <= 0:
        raise ValueError("mass > 0, speed >= 0, charge != 0, and magnetic_field > 0 are required")
    return mass * speed / (abs(charge) * magnetic_field)

def magnetic_force_magnitude(charge: float, speed: float, magnetic_field: float) -> float:
    return abs(charge) * speed * magnetic_field

def cyclotron_period(mass: float, charge: float, magnetic_field: float) -> float:
    if mass <= 0 or charge == 0 or magnetic_field <= 0:
        raise ValueError("mass > 0, charge != 0, and magnetic_field > 0 are required")
    return 2 * np.pi * mass / (abs(charge) * magnetic_field)
