"""Streamlit entry point for Magnetism Lab."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from modules.component_loader import render_custom_app


APP_DIR = Path(__file__).parent


st.set_page_config(
    page_title="Magnetism Lab",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def hide_streamlit_chrome() -> None:
    """Use Streamlit as a deployment shell for the custom simulator UI."""
    st.markdown(
        """
        <style>
        #MainMenu,
        header,
        footer,
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        html,
        body,
        .stApp {
            background: #070A12;
            overflow: hidden;
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        .main {
            background: #070A12;
        }

        .main .block-container {
            max-width: none;
            padding: 0;
        }

        [data-testid="stVerticalBlock"],
        [data-testid="stElementContainer"] {
            gap: 0 !important;
        }

        iframe {
            display: block;
            border: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Render Magnetism Lab."""
    hide_streamlit_chrome()
    render_custom_app(APP_DIR / "custom_app.html")


if __name__ == "__main__":
    main()
