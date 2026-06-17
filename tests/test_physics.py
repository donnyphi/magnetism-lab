"""Tests for Magnetism Lab physics helpers."""

import numpy as np

from utils.physics import (
    charged_particle_radius,
    direction_to_vector,
    magnetic_force_direction,
    wire_field_strength,
)


def test_direction_to_vector_positive_x() -> None:
    assert np.allclose(direction_to_vector("+x"), np.array([1.0, 0.0, 0.0]))


def test_positive_x_cross_positive_y_is_positive_z() -> None:
    assert magnetic_force_direction("positive", "+x", "+y") == "+z"


def test_negative_charge_reverses_force_direction() -> None:
    assert magnetic_force_direction("negative", "+x", "+y") == "-z"


def test_parallel_velocity_and_field_gives_zero_force() -> None:
    assert magnetic_force_direction("positive", "+x", "+x") == "zero"


def test_wire_field_decreases_when_radius_increases() -> None:
    near = wire_field_strength(current=5.0, radius=0.5)
    far = wire_field_strength(current=5.0, radius=1.0)
    assert far < near
    assert np.isclose(far, near / 2)


def test_charged_particle_radius_increases_with_speed() -> None:
    slow = charged_particle_radius(mass=1.0, speed=2.0, charge=1.0, magnetic_field=2.0)
    fast = charged_particle_radius(mass=1.0, speed=4.0, charge=1.0, magnetic_field=2.0)
    assert fast > slow


def test_charged_particle_radius_decreases_with_magnetic_field_strength() -> None:
    weak = charged_particle_radius(mass=1.0, speed=4.0, charge=1.0, magnetic_field=1.0)
    strong = charged_particle_radius(mass=1.0, speed=4.0, charge=1.0, magnetic_field=2.0)
    assert strong < weak
