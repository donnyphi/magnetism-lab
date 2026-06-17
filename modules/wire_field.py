import streamlit as st
from utils.physics import wire_field_strength
from utils.plotting import plot_wire_field

def render():
    st.header("Magnetic Field Around a Wire")
    st.write("A long straight wire produces circular magnetic field lines: **B = μ₀I / (2πr)**.")
    current = st.slider("Current I (A)", 0.1, 20.0, 5.0)
    radius = st.slider("Distance r from wire (m)", 0.01, 5.0, 1.0)
    direction = st.radio("Current direction", ["out of page", "into page"], horizontal=True)
    B = wire_field_strength(current, radius)
    st.metric("Magnetic field strength", f"{B:.3e} T")
    st.pyplot(plot_wire_field(direction))
    st.info("Out of page gives counterclockwise field lines. Into page gives clockwise field lines. If distance doubles, field strength is cut in half.")
