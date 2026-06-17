import streamlit as st
from modules import right_hand_rule, wire_field, charged_particle, practice

st.set_page_config(page_title="Magnetism Lab", page_icon="🧲", layout="wide")
st.title("🧲 Magnetism Lab")
st.caption("Interactive E&M simulations for magnetic fields, right-hand rules, and charged particle motion.")

page = st.sidebar.radio("Navigate", ["Home", "Right-Hand Rule", "Field Around a Wire", "Charged Particle Motion", "Practice Mode"])

if page == "Home":
    st.header("Learn magnetism by seeing it move")
    st.write("Magnetism Lab is a freshman-level E&M learning platform built around visualizations, sliders, and practice questions.")
    c1, c2, c3 = st.columns(3)
    c1.subheader("Right-Hand Rule")
    c1.write("Practice force directions using F = q(v × B).")
    c2.subheader("Wire Fields")
    c2.write("Explore circular magnetic fields around current-carrying wires.")
    c3.subheader("Particle Motion")
    c3.write("Simulate charged particles curving in uniform magnetic fields.")
    st.markdown("### Concepts covered")
    st.write("Cross products, magnetic force, field lines, circular motion, cyclotron period, and beginner E&M intuition.")
elif page == "Right-Hand Rule":
    right_hand_rule.render()
elif page == "Field Around a Wire":
    wire_field.render()
elif page == "Charged Particle Motion":
    charged_particle.render()
else:
    practice.render()
