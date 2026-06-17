from utils.physics import magnetic_force_direction, wire_field_strength, charged_particle_radius

def test_positive_x_cross_y_is_z():
    assert magnetic_force_direction("positive", "+x", "+y") == "+z"

def test_negative_charge_reverses_direction():
    assert magnetic_force_direction("negative", "+x", "+y") == "-z"

def test_parallel_velocity_and_field_zero():
    assert magnetic_force_direction("positive", "+x", "+x") == "zero"

def test_wire_field_decreases_with_radius():
    assert wire_field_strength(5, 2) < wire_field_strength(5, 1)

def test_particle_radius_increases_with_speed():
    assert charged_particle_radius(1, 10, 1, 2) > charged_particle_radius(1, 5, 1, 2)

def test_particle_radius_decreases_with_magnetic_field():
    assert charged_particle_radius(1, 5, 1, 4) < charged_particle_radius(1, 5, 1, 2)
