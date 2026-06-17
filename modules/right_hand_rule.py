import streamlit as st
import numpy as np
from utils.physics import direction_to_vector, magnetic_force_direction
from utils.plotting import plot_vectors

def render():
    st.header("Right-Hand Rule Trainer")
    st.write("Magnetic force on a moving charge follows **F = q(v × B)**.")
    charge = st.selectbox("Charge sign", ["positive", "negative"])
    v_dir = st.selectbox("Velocity direction", ["+x", "-x", "+y", "-y", "+z", "-z"], index=0)
    b_dir = st.selectbox("Magnetic field direction", ["+x", "-x", "+y", "-y", "+z", "-z"], index=2)
    f_dir = magnetic_force_direction(charge, v_dir, b_dir)
    if f_dir == "zero":
        st.success("The magnetic force is zero because velocity and magnetic field are parallel or anti-parallel.")
        f = np.array([0,0,0])
    else:
        st.success(f"For a {charge} charge with v in {v_dir} and B in {b_dir}, the force points in **{f_dir}**.")
        f = direction_to_vector(f_dir)
    st.pyplot(plot_vectors(direction_to_vector(v_dir), direction_to_vector(b_dir), f))
    st.info("For a positive charge, point your fingers along velocity and curl toward B. Your thumb gives force. Negative charges reverse the direction.")
