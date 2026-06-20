"""Magnetism Lab — interactive E&M learning app (Streamlit entry point)."""
import streamlit as st

from modules import charged_particle, home, practice, right_hand_rule, wire_field
from utils import ui

st.set_page_config(page_title="Magnetism Lab", page_icon="🧲", layout="wide")
ui.inject_global_styles()

# Each page maps a label (shown in the sidebar) to the module that renders it.
PAGES = {
    "🏠 Home": home.render,
    "🖐️ Right-Hand Rule": right_hand_rule.render,
    "🧲 Field Around a Wire": wire_field.render,
    "🌀 Charged Particle Motion": charged_particle.render,
    "🎯 Practice Mode": practice.render,
}

# `page` is the single source of truth for navigation. Module cards on the home
# page set it via ui.navigate_to (an on_click callback that runs before the
# sidebar radio is rebuilt), and the sidebar radio is bound to the same key.
if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Home"

st.sidebar.title("🧲 Magnetism Lab")
st.sidebar.caption("Interactive E&M for first-year physics.")
st.sidebar.radio("Navigate", list(PAGES), key="page", label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.caption("Built by Donny Nguyen · learn E&M by doing.")

PAGES[st.session_state["page"]]()
