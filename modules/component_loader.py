"""Helpers for rendering the custom Magnetism Lab interface."""

from __future__ import annotations

from pathlib import Path

from streamlit.components.v1 import html


def render_custom_app(source_path: Path, *, height: int = 760) -> None:
    """Render the custom HTML/CSS/JS simulator in a Streamlit component."""
    html(source_path.read_text(encoding="utf-8"), height=height, scrolling=True)
