"""Practice Mode — a small, self-contained quiz engine for Magnetism Lab.

Questions live in :data:`QUESTIONS` as plain dicts. Numeric answers are computed
from :mod:`utils.physics` so the quiz can never disagree with the simulations.
Progress (score, streak, accuracy, per-topic stats) is tracked in
``st.session_state`` and summarized at the end.
"""
from __future__ import annotations

import streamlit as st

from utils import ui
from utils.physics import (
    charged_particle_radius,
    cyclotron_period,
    magnetic_force_magnitude,
    wire_field_strength,
)

# Topic -> the module a struggling student should revisit.
TOPIC_MODULE = {
    "Right-hand rule": "🖐️ Right-Hand Rule",
    "Wire field direction": "🧲 Field Around a Wire",
    "Wire field magnitude": "🧲 Field Around a Wire",
    "Charged particle radius": "🌀 Charged Particle Motion",
    "Conceptual magnetism": "🌀 Charged Particle Motion",
}

# Multiple-choice helper to keep the bank readable.
def _mc(topic, difficulty, q, choices, a, hint1, hint2, exp, concept):
    return {"type": "mc", "topic": topic, "difficulty": difficulty, "q": q,
            "choices": choices, "a": a, "hint1": hint1, "hint2": hint2,
            "exp": exp, "concept": concept}


def _num(topic, difficulty, q, a, tol, unit, hint1, hint2, exp, concept):
    return {"type": "num", "topic": topic, "difficulty": difficulty, "q": q,
            "a": a, "tol": tol, "unit": unit, "hint1": hint1, "hint2": hint2,
            "exp": exp, "concept": concept}


QUESTIONS = [
    # --- Right-hand rule ------------------------------------------------
    _mc("Right-hand rule", "Easy",
        "Positive charge: v = +x, B = +y. Which way does the force point?",
        ["+z", "-z", "zero", "+x"], "+z",
        "Use your right hand: fingers along +x, curl toward +y.",
        "Compute +x × +y using the cross product.",
        "For a positive charge, +x × +y = +z.", "Cross products"),
    _mc("Right-hand rule", "Medium",
        "Negative charge: v = +x, B = +y. Which way does the force point?",
        ["+z", "-z", "zero", "+y"], "-z",
        "Find the positive-charge answer first, then flip it.",
        "+x × +y = +z, and a negative charge reverses the result.",
        "The positive case gives +z, so a negative charge gives -z.",
        "Charge sign reversal"),
    _mc("Right-hand rule", "Easy",
        "If v is parallel to B, the magnetic force is…",
        ["maximum", "zero", "negative", "infinite"], "zero",
        "Think about the angle between v and B.",
        "F = |q|vB·sin(θ), and here θ = 0°.",
        "When θ = 0°, sin(θ) = 0, so the force is zero.", "Lorentz force"),
    _mc("Right-hand rule", "Medium",
        "Positive charge: v = +y, B = +z. Which way does the force point?",
        ["+x", "-x", "+z", "zero"], "+x",
        "Right hand: fingers along +y, curl toward +z.",
        "Compute +y × +z.",
        "+y × +z = +x for a positive charge.", "Cross products"),
    _mc("Right-hand rule", "Challenge",
        "Swapping the order of a cross product (B × v instead of v × B)…",
        ["gives the same direction", "reverses the direction",
         "always gives zero", "doubles the magnitude"], "reverses the direction",
        "Cross products are not commutative.",
        "v × B = −(B × v).",
        "Reversing the order of a cross product flips its sign, so the force "
        "points the opposite way.", "Cross products"),

    # --- Wire field direction -------------------------------------------
    _mc("Wire field direction", "Easy",
        "Current straight out of the page (⊙) gives field lines that circulate…",
        ["clockwise", "counter-clockwise", "straight up", "in toward the wire"],
        "counter-clockwise",
        "Point your right thumb out of the page toward yourself.",
        "Curl your fingers around the wire; they show the field direction.",
        "Thumb out of the page → fingers curl counter-clockwise.",
        "Right-hand rule for wires"),
    _mc("Wire field direction", "Easy",
        "Current into the page (⊗) gives field lines that circulate…",
        ["clockwise", "counter-clockwise", "radially outward", "zero"],
        "clockwise",
        "Point your right thumb into the page.",
        "Curl your fingers around the wire.",
        "Thumb into the page → fingers curl clockwise.",
        "Right-hand rule for wires"),
    _mc("Wire field direction", "Medium",
        "The symbol ⊗ next to a wire means the current is…",
        ["coming toward you", "going away from you", "turned off",
         "alternating"], "going away from you",
        "Picture an arrow as a dart.",
        "⊗ is the tail feathers of an arrow flying away.",
        "A cross (⊗) is the tail of an arrow heading away into the page.",
        "Dot/cross notation"),
    _mc("Wire field direction", "Medium",
        "The symbol ⊙ next to a wire means the current is…",
        ["coming toward you", "going away from you", "stopped",
         "perpendicular to the page edge"], "coming toward you",
        "Picture the tip of an arrow.",
        "⊙ is the point of an arrow flying toward you.",
        "A dot (⊙) is the tip of an arrow coming out toward you.",
        "Dot/cross notation"),

    # --- Wire field magnitude -------------------------------------------
    _mc("Wire field magnitude", "Easy",
        "For a straight wire, if distance r doubles, B becomes…",
        ["twice as large", "half as large", "four times as large", "unchanged"],
        "half as large",
        "B depends on 1/r.",
        "B = μ₀I/(2πr); replace r with 2r.",
        "B ∝ 1/r, so doubling r halves B.", "Field around a wire"),
    _mc("Wire field magnitude", "Medium",
        "To make the field around a wire stronger, you can…",
        ["increase the current", "move farther away",
         "decrease the current", "make the wire longer"], "increase the current",
        "Look at what's in the numerator of the formula.",
        "B = μ₀I/(2πr): I is on top, r is on the bottom.",
        "More current means a stronger field; moving away weakens it.",
        "Field around a wire"),
    _mc("Wire field magnitude", "Challenge",
        "Why can't you use B = μ₀I/(2πr) at r = 0?",
        ["The field is actually zero there",
         "Division by zero — the formula diverges",
         "Current reverses at the center", "μ₀ becomes negative"],
        "Division by zero — the formula diverges",
        "Think about what happens to 1/r as r shrinks.",
        "As r → 0, 1/r → ∞.",
        "The ideal formula blows up at r = 0; a real wire has thickness and a "
        "different field inside it.", "Field around a wire"),
    _num("Wire field magnitude", "Challenge",
         "A wire carries I = 10 A. Find B at r = 0.5 m. Answer in µT.",
         wire_field_strength(10, 0.5) * 1e6, 0.05, "µT",
         "Use the wire-field formula and convert teslas to microteslas.",
         "B = μ₀I/(2πr) with μ₀ = 4π×10⁻⁷; then ×10⁶ for µT.",
         f"B = μ₀(10)/(2π·0.5) = {wire_field_strength(10, 0.5)*1e6:.2f} µT.",
         "Field around a wire"),

    # --- Charged particle radius ----------------------------------------
    _mc("Charged particle radius", "Easy",
        "Increasing the magnetic field strength makes the orbit radius…",
        ["larger", "smaller", "unchanged", "infinite"], "smaller",
        "Where does B sit in r = mv/(|q|B)?",
        "B is in the denominator.",
        "B is in the denominator, so a stronger field gives a tighter circle.",
        "Circular motion"),
    _mc("Charged particle radius", "Easy",
        "Increasing the particle's speed makes the orbit radius…",
        ["larger", "smaller", "zero", "unchanged"], "larger",
        "Where does v sit in r = mv/(|q|B)?",
        "v is in the numerator.",
        "Speed is in the numerator, so a faster particle orbits in a wider "
        "circle.", "Circular motion"),
    _mc("Charged particle radius", "Medium",
        "A heavier particle (larger m), same field and speed, has a radius "
        "that is…",
        ["larger", "smaller", "the same", "zero"], "larger",
        "More mass means more inertia — harder to turn.",
        "m is in the numerator of r = mv/(|q|B).",
        "Mass is in the numerator, so a heavier particle makes a bigger circle.",
        "Circular motion"),
    _num("Charged particle radius", "Medium",
         "Find the orbit radius for m = 2 kg, v = 10 m/s, |q| = 2 C, B = 5 T. "
         "Answer in metres.",
         charged_particle_radius(2, 10, 2, 5), 0.05, "m",
         "Plug into the radius formula.",
         "r = mv/(|q|B) = (2·10)/(2·5).",
         f"r = (2·10)/(2·5) = {charged_particle_radius(2, 10, 2, 5):.2f} m.",
         "Circular motion"),
    _num("Charged particle radius", "Challenge",
         "Find the cyclotron period for m = 1 kg, |q| = 1 C, B = 2 T. "
         "Answer in seconds.",
         cyclotron_period(1, 1, 2), 0.05, "s",
         "The period doesn't depend on speed or radius.",
         "T = 2πm/(|q|B) = 2π·1/(1·2).",
         f"T = 2π/(2) = {cyclotron_period(1, 1, 2):.3f} s.", "Cyclotron period"),

    # --- Conceptual magnetism -------------------------------------------
    _mc("Conceptual magnetism", "Easy",
        "The magnetic force on a moving charge is always perpendicular to…",
        ["velocity", "mass", "charge sign", "time"], "velocity",
        "Cross products produce a perpendicular vector.",
        "q(v × B) is perpendicular to both v and B.",
        "F = q(v × B) is perpendicular to the velocity, which is why the path "
        "curves.", "Lorentz force"),
    _mc("Conceptual magnetism", "Medium",
        "Does a magnetic field do work on a charge in uniform circular motion?",
        ["yes", "no", "only if positive", "only if negative"], "no",
        "Work needs a force component along the motion.",
        "The force is perpendicular to the velocity the whole time.",
        "A perpendicular force changes direction, not speed, so it does no work.",
        "Work–energy"),
    _mc("Conceptual magnetism", "Medium",
        "A positive and a negative charge enter the same field with the same "
        "velocity. Their circular paths…",
        ["curve the same way", "curve in opposite directions",
         "are both straight", "have different radii"],
        "curve in opposite directions",
        "The force direction flips with the sign of the charge.",
        "F = q(v × B): flip q and you flip F.",
        "Opposite charges feel opposite forces, so they curve in opposite "
        "senses (same radius, mirror-image circles).", "Charge sign reversal"),
    _num("Conceptual magnetism", "Easy",
         "Find the force magnitude for |q| = 2 C, v = 3 m/s, B = 4 T "
         "(v ⟂ B). Answer in newtons.",
         magnetic_force_magnitude(2, 3, 4), 0.05, "N",
         "Use F = |q|vB for perpendicular velocity and field.",
         "F = |q|vB = 2·3·4.",
         f"F = 2·3·4 = {magnetic_force_magnitude(2, 3, 4):.0f} N.",
         "Lorentz force"),
    _mc("Conceptual magnetism", "Challenge",
        "If B = 0 everywhere, a moving charge will…",
        ["move in a circle", "move in a straight line", "stop immediately",
         "spiral inward"], "move in a straight line",
        "No field means no magnetic force.",
        "F = |q|vB = 0 when B = 0.",
        "With no magnetic force, there's nothing to bend the path, so the "
        "charge travels in a straight line.", "Lorentz force"),
]

DIFFICULTY_BADGE = {"Easy": "🟢 Easy", "Medium": "🟡 Medium", "Challenge": "🔴 Challenge"}


def render() -> None:
    ui.section_header(
        "Practice Mode",
        f"{len(QUESTIONS)} questions across five topics. Predict, use hints if "
        "you need them, and track your mastery.",
    )

    _init_state()
    _render_scoreboard()

    # --- Filters ---------------------------------------------------------
    topics = ["All topics"] + sorted({q["topic"] for q in QUESTIONS})
    difficulties = ["All", "Easy", "Medium", "Challenge"]
    f1, f2 = st.columns(2)
    topic_filter = f1.selectbox("Filter by topic", topics)
    diff_filter = f2.selectbox("Filter by difficulty", difficulties)

    shown = [
        (i, q) for i, q in enumerate(QUESTIONS)
        if (topic_filter == "All topics" or q["topic"] == topic_filter)
        and (diff_filter == "All" or q["difficulty"] == diff_filter)
    ]
    if not shown:
        ui.note("No questions match those filters. Try widening them.")
    for i, q in shown:
        _render_question(i, q)

    st.markdown("---")
    _render_summary()
    if st.button("Reset session"):
        _reset_state()
        st.rerun()


# --- Session state --------------------------------------------------------
def _init_state() -> None:
    defaults = {
        "p_results": {},       # idx -> bool correct (latest attempt)
        "p_streak": 0,
        "p_best_streak": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _reset_state() -> None:
    for k in ("p_results", "p_streak", "p_best_streak"):
        st.session_state.pop(k, None)
    # Clear any per-question widget state.
    for k in list(st.session_state.keys()):
        if k.startswith(("ans_", "hint_")):
            st.session_state.pop(k, None)


def _record(idx: int, correct: bool) -> None:
    st.session_state.p_results[idx] = correct
    if correct:
        st.session_state.p_streak += 1
        st.session_state.p_best_streak = max(
            st.session_state.p_best_streak, st.session_state.p_streak)
    else:
        st.session_state.p_streak = 0


# --- Rendering pieces -----------------------------------------------------
def _render_scoreboard() -> None:
    results = st.session_state.p_results
    attempted = len(results)
    correct = sum(1 for v in results.values() if v)
    accuracy = (correct / attempted * 100) if attempted else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score", f"{correct} / {len(QUESTIONS)}")
    c2.metric("Attempted", f"{attempted}")
    c3.metric("Accuracy", f"{accuracy:.0f}%")
    c4.metric("Streak", f"🔥 {st.session_state.p_streak}",
              help=f"Best this session: {st.session_state.p_best_streak}")


def _render_question(idx: int, q: dict) -> None:
    prior = st.session_state.p_results.get(idx)
    mark = "" if prior is None else (" ✅" if prior else " ❌")
    header = f"{DIFFICULTY_BADGE[q['difficulty']]} · {q['topic']} — {q['q']}{mark}"

    with st.expander(header):
        # Two-tier hint system.
        h1, h2 = st.columns(2)
        if h1.button("💡 Hint 1 (intuition)", key=f"hint1_{idx}"):
            st.info(q["hint1"])
        if h2.button("📐 Hint 2 (setup)", key=f"hint2_{idx}"):
            st.info(q["hint2"])

        if q["type"] == "mc":
            choice = st.radio("Choose one", q["choices"], index=None,
                              key=f"ans_{idx}")
            if st.button("Submit", key=f"submit_{idx}"):
                if choice is None:
                    st.warning("Pick an answer first.")
                else:
                    _grade(idx, q, choice == q["a"])
        else:  # numeric
            val = st.number_input(f"Your answer ({q['unit']})", value=None,
                                  format="%.4f", key=f"ans_{idx}")
            if st.button("Submit", key=f"submit_{idx}"):
                if val is None:
                    st.warning("Enter a number first.")
                else:
                    _grade(idx, q, abs(val - q["a"]) <= q["tol"])


def _grade(idx: int, q: dict, correct: bool) -> None:
    _record(idx, correct)
    if q["type"] == "num":
        answer_text = f"{q['a']:.3f} {q['unit']}"
    else:
        answer_text = q["a"]
    if correct:
        st.success(f"✅ Correct! {q['exp']}")
    else:
        st.error(f"❌ Not quite. The answer is **{answer_text}**. {q['exp']}")
    st.caption(f"Related concept: **{q['concept']}**")


def _render_summary() -> None:
    results = st.session_state.p_results
    if not results:
        ui.note("Answer a few questions to unlock your <b>session summary</b> — "
                "your strongest and weakest topics, plus what to review next.")
        return

    # Per-topic accuracy.
    stats: dict[str, list[int]] = {}
    for idx, correct in results.items():
        topic = QUESTIONS[idx]["topic"]
        s = stats.setdefault(topic, [0, 0])
        s[1] += 1
        if correct:
            s[0] += 1

    ui.section_header("Session summary")
    rows_topic, rows_acc = [], []
    for topic, (c, n) in sorted(stats.items()):
        rows_topic.append(topic)
        rows_acc.append(f"{c}/{n}  ({c / n * 100:.0f}%)")
    st.table({"Topic": rows_topic, "Score": rows_acc})

    ranked = sorted(stats.items(), key=lambda kv: kv[1][0] / kv[1][1])
    weakest, (wc, wn) = ranked[0]
    strongest, (sc, sn) = ranked[-1]

    cols = st.columns(2)
    cols[0].success(f"💪 Strongest: **{strongest}** "
                    f"({sc / sn * 100:.0f}%)")
    cols[1].warning(f"📚 Needs work: **{weakest}** "
                    f"({wc / wn * 100:.0f}%)")
    ui.note(f"Recommended next step: revisit the <b>{TOPIC_MODULE[weakest]}</b> "
            f"module to shore up <b>{weakest}</b>, then come back and try those "
            "questions again.")
