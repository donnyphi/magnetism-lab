"""Unit tests for the physics helpers in :mod:`utils.physics`."""
import math

import numpy as np
import pytest

from utils.physics import (
    MU_0,
    charged_particle_radius,
    cyclotron_frequency,
    cyclotron_period,
    direction_to_vector,
    is_zero_force,
    magnetic_force_direction,
    magnetic_force_magnitude,
    vector_to_direction,
    wire_field_strength,
)


# --- Right-hand rule / cross products ------------------------------------
def test_positive_x_cross_y_is_z():
    assert magnetic_force_direction("positive", "+x", "+y") == "+z"


def test_y_cross_z_is_x():
    assert magnetic_force_direction("positive", "+y", "+z") == "+x"


def test_z_cross_x_is_y():
    assert magnetic_force_direction("positive", "+z", "+x") == "+y"


def test_swapping_order_reverses_direction():
    assert magnetic_force_direction("positive", "+y", "+x") == "-z"


def test_negative_charge_reverses_direction():
    assert magnetic_force_direction("negative", "+x", "+y") == "-z"


def test_parallel_velocity_and_field_zero():
    assert magnetic_force_direction("positive", "+x", "+x") == "zero"


def test_antiparallel_velocity_and_field_zero():
    assert magnetic_force_direction("positive", "+x", "-x") == "zero"


def test_is_zero_force_detects_parallel():
    assert is_zero_force("+x", "+x")
    assert is_zero_force("+y", "-y")
    assert not is_zero_force("+x", "+y")


def test_direction_vector_roundtrip():
    for label in ("+x", "-x", "+y", "-y", "+z", "-z"):
        assert vector_to_direction(direction_to_vector(label)) == label


def test_vector_to_direction_zero():
    assert vector_to_direction(np.zeros(3)) == "zero"


def test_unknown_direction_raises():
    with pytest.raises(ValueError):
        direction_to_vector("+w")


# --- Wire field ----------------------------------------------------------
def test_wire_field_decreases_with_radius():
    assert wire_field_strength(5, 2) < wire_field_strength(5, 1)


def test_wire_field_inverse_distance_relationship():
    # Doubling the distance should halve the field.
    assert wire_field_strength(5, 2) == pytest.approx(wire_field_strength(5, 1) / 2)
    # Tripling the distance gives one third.
    assert wire_field_strength(5, 3) == pytest.approx(wire_field_strength(5, 1) / 3)


def test_wire_field_scales_with_current():
    assert wire_field_strength(10, 1) == pytest.approx(2 * wire_field_strength(5, 1))


def test_wire_field_known_value():
    # B = μ0 I / (2π r)
    assert wire_field_strength(10, 0.5) == pytest.approx(MU_0 * 10 / (2 * math.pi * 0.5))


def test_wire_field_zero_radius_raises():
    with pytest.raises(ValueError):
        wire_field_strength(5, 0)


# --- Charged particle radius --------------------------------------------
def test_particle_radius_formula():
    assert charged_particle_radius(2, 10, 2, 5) == pytest.approx(2.0)


def test_particle_radius_increases_with_speed():
    assert charged_particle_radius(1, 10, 1, 2) > charged_particle_radius(1, 5, 1, 2)


def test_particle_radius_increases_with_mass():
    assert charged_particle_radius(2, 5, 1, 2) > charged_particle_radius(1, 5, 1, 2)


def test_particle_radius_decreases_with_magnetic_field():
    assert charged_particle_radius(1, 5, 1, 4) < charged_particle_radius(1, 5, 1, 2)


def test_particle_radius_decreases_with_charge():
    assert charged_particle_radius(1, 5, 4, 2) < charged_particle_radius(1, 5, 1, 2)


def test_particle_radius_sign_independent():
    assert charged_particle_radius(1, 5, -2, 2) == charged_particle_radius(1, 5, 2, 2)


def test_particle_radius_zero_speed_is_zero():
    assert charged_particle_radius(1, 0, 1, 2) == 0.0


@pytest.mark.parametrize("m,v,q,b", [(0, 5, 1, 2), (1, 5, 0, 2), (1, 5, 1, 0)])
def test_particle_radius_invalid_inputs_raise(m, v, q, b):
    with pytest.raises(ValueError):
        charged_particle_radius(m, v, q, b)


# --- Force magnitude -----------------------------------------------------
def test_force_magnitude_formula():
    assert magnetic_force_magnitude(2, 3, 4) == pytest.approx(24.0)


def test_force_magnitude_sign_independent():
    assert magnetic_force_magnitude(-2, 3, 4) == magnetic_force_magnitude(2, 3, 4)


def test_force_magnitude_angle_dependence():
    perp = magnetic_force_magnitude(2, 3, 4, angle_deg=90)
    half = magnetic_force_magnitude(2, 3, 4, angle_deg=30)
    assert perp == pytest.approx(24.0)
    assert half == pytest.approx(24.0 * 0.5)


def test_force_magnitude_parallel_is_zero():
    assert magnetic_force_magnitude(2, 3, 4, angle_deg=0) == pytest.approx(0.0)


def test_force_magnitude_zero_inputs():
    assert magnetic_force_magnitude(0, 3, 4) == 0.0
    assert magnetic_force_magnitude(2, 0, 4) == 0.0
    assert magnetic_force_magnitude(2, 3, 0) == 0.0


# --- Cyclotron period / frequency ---------------------------------------
def test_cyclotron_period_formula():
    assert cyclotron_period(1, 1, 2) == pytest.approx(math.pi)


def test_cyclotron_period_independent_of_speed():
    # Period has no speed term, so two speeds give the same value (sanity).
    assert cyclotron_period(2, 3, 4) == pytest.approx(2 * math.pi * 2 / (3 * 4))


def test_cyclotron_frequency_formula():
    assert cyclotron_frequency(2, 3, 4) == pytest.approx(3 * 4 / 2)


def test_cyclotron_period_and_frequency_consistent():
    # ω = 2π / T
    m, q, b = 2.0, 1.5, 3.0
    assert cyclotron_frequency(m, q, b) == pytest.approx(
        2 * math.pi / cyclotron_period(m, q, b))


@pytest.mark.parametrize("m,q,b", [(0, 1, 2), (1, 0, 2), (1, 1, 0)])
def test_cyclotron_invalid_inputs_raise(m, q, b):
    with pytest.raises(ValueError):
        cyclotron_period(m, q, b)
    with pytest.raises(ValueError):
        cyclotron_frequency(m, q, b)
