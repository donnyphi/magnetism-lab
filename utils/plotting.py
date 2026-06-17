"""Plotting helpers for Magnetism Lab."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def plot_vectors(v, b, f):
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="3d")
    vectors = [(v, "v"), (b, "B"), (f, "F")]
    for vec, label in vectors:
        vec = np.asarray(vec, dtype=float)
        if np.linalg.norm(vec) > 1e-12:
            ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], length=1, normalize=True)
            ax.text(vec[0], vec[1], vec[2], label)
    ax.set_xlim([-1, 1]); ax.set_ylim([-1, 1]); ax.set_zlim([-1, 1])
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.set_title("Right-hand rule vectors")
    return fig

def plot_wire_field(current_direction: str):
    x = np.linspace(-2, 2, 25)
    y = np.linspace(-2, 2, 25)
    X, Y = np.meshgrid(x, y)
    R2 = X**2 + Y**2
    R2[R2 == 0] = np.nan
    if current_direction == "out of page":
        U, V = -Y / R2, X / R2
    else:
        U, V = Y / R2, -X / R2
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.streamplot(X, Y, U, V, density=1.4)
    ax.scatter([0], [0], s=120)
    ax.text(0.08, 0.08, "I")
    ax.set_aspect("equal")
    ax.set_title(f"Magnetic field around a wire: current {current_direction}")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    return fig

def plot_particle_circle(radius: float, charge_sign: str):
    theta = np.linspace(0, 2*np.pi, 500)
    direction = -1 if charge_sign == "positive" else 1
    x = radius * np.cos(direction * theta)
    y = radius * np.sin(direction * theta)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y)
    ax.scatter([x[0]], [y[0]], s=60)
    ax.set_aspect("equal")
    ax.set_title("Circular motion in uniform magnetic field")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    return fig
