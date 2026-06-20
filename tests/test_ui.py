"""Smoke tests for the UI component layer.

These guard against the kind of regression that broke deployment before: a page
calling a UI helper that no longer exists. They only check that the public
component API is importable and callable — no Streamlit runtime is needed.
"""
import inspect

from utils import ui

# The components the pages rely on. If any of these disappears or is renamed
# without updating call sites, a page will crash at runtime — so assert here.
REQUIRED = [
    "inject_global_styles",
    "inject_global_css",  # backwards-compatible alias
    "top_nav",
    "navigate_to",
    "hero_section",
    "page_hero",
    "section_header",
    "divider",
    "module_card",
    "module_cards",
    "card_grid",
    "learning_path",
    "steps_card",
    "formula_card",
    "formula_grid",
    "summary_chips",
    "concept_chips",
    "callout_card",
    "stat_card",
    "stat_cards",
    "examples_table",
    "plot_shell",
    "control_panel",
    "practice_question_card",
    "hint_card",
    "result_card",
    "intuition_check",
    "next_module_cta",
    "footer",
]


def test_required_components_exist_and_are_callable():
    for name in REQUIRED:
        assert hasattr(ui, name), f"utils.ui is missing '{name}'"
        assert callable(getattr(ui, name)), f"utils.ui.{name} is not callable"


def test_inject_global_styles_is_the_canonical_name():
    # app.py calls inject_global_styles(); make sure it is a real function and
    # that the legacy alias points at the same object.
    assert inspect.isfunction(ui.inject_global_styles)
    assert ui.inject_global_css is ui.inject_global_styles


def test_pure_html_helpers_return_strings():
    # The string-returning builders should produce HTML without a Streamlit run.
    assert ui.module_card("🧲", "Title", "Body").startswith("<div")
    assert "ml-stat" in ui.stat_card("Score", "5")
