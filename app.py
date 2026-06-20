"""Magnetism Lab — interactive E&M learning app (Streamlit entry point)."""
import streamlit as st

from modules import charged_particle, home, practice, right_hand_rule, wire_field
from utils import ui

st.set_page_config(page_title="Magnetism Lab", page_icon="🧲", layout="wide")
ui.inject_global_css()

# Each page maps a sidebar label to the module that renders it.
PAGES = {
    "🏠 Home": home.render,
    "🖐️ Right-Hand Rule": right_hand_rule.render,
    "🧲 Field Around a Wire": wire_field.render,
    "🌀 Charged Particle Motion": charged_particle.render,
    "🎯 Practice Mode": practice.render,
}

st.sidebar.title("🧲 Magnetism Lab")
st.sidebar.caption("Interactive E&M for first-year physics.")
choice = st.sidebar.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.caption("Built by Donny Nguyen · made for learning E&M by doing.")

PAGES[choice]()
