"""Magnetism Lab — interactive E&M learning app (Streamlit entry point)."""
import streamlit as st

from modules import charged_particle, home, practice, right_hand_rule, wire_field
from utils import ui

st.set_page_config(
    page_title="Magnetism Lab",
    page_icon="🧲",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject the global stylesheet. The helper is exposed under both
# `inject_global_styles` and the older `inject_global_css` name, so resolve it
# defensively to stay robust across cached deployments.
_inject_styles = getattr(ui, "inject_global_styles", None) or getattr(
    ui, "inject_global_css", None
)
if _inject_styles is not None:
    _inject_styles()

# Each page maps a label (shown in the top nav) to the module that renders it.
PAGES = {
    "🏠 Home": home.render,
    "🖐️ Right-Hand Rule": right_hand_rule.render,
    "🧲 Field Around a Wire": wire_field.render,
    "🌀 Charged Particle Motion": charged_particle.render,
    "🎯 Practice Mode": practice.render,
}

# `page` is the single source of truth for navigation. The top nav and the
# home-page module cards set it via ui.navigate_to (an on_click callback that
# runs before the nav is rebuilt). A hidden sidebar radio is bound to the same
# key as an accessible fallback.
if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Home"

with st.sidebar:
    st.radio("Navigate", list(PAGES), key="page")

ui.top_nav(list(PAGES), active=st.session_state["page"])
PAGES[st.session_state["page"]]()
ui.footer()
