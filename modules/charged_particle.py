import streamlit as st
from utils.physics import charged_particle_radius, magnetic_force_magnitude, cyclotron_period
from utils.plotting import plot_particle_circle

def render():
    st.header("Charged Particle Motion")
    st.write("For velocity perpendicular to a uniform magnetic field, the particle moves in a circle.")
    charge_sign = st.selectbox("Charge sign", ["positive", "negative"])
    q_mag = st.slider("Charge magnitude |q| (C)", 0.1, 5.0, 1.0)
    mass = st.slider("Mass m (kg)", 0.1, 10.0, 1.0)
    speed = st.slider("Speed v (m/s)", 0.1, 20.0, 5.0)
    B = st.slider("Magnetic field B (T)", 0.1, 10.0, 2.0)
    q = q_mag if charge_sign == "positive" else -q_mag
    r = charged_particle_radius(mass, speed, q, B)
    F = magnetic_force_magnitude(q, speed, B)
    T = cyclotron_period(mass, q, B)
    col1, col2, col3 = st.columns(3)
    col1.metric("Radius", f"{r:.3f} m")
    col2.metric("Force", f"{F:.3f} N")
    col3.metric("Period", f"{T:.3f} s")
    st.pyplot(plot_particle_circle(r, charge_sign))
    st.info("Stronger B makes a tighter circle. Faster speed or larger mass makes a wider circle. Negative charge curves the opposite way.")
