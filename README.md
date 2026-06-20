# 🧲 Magnetism Lab

**Interactive E&M simulations for right-hand rules, magnetic fields, and charged particle motion.**

Magnetism Lab is a freshman-friendly physics learning platform that turns magnetic
field equations into interactive visual intuition. Move sliders, predict answers
before revealing them, and test yourself in a built-in practice mode — all in the
browser.

> Built by **Donny Nguyen** ([@donnyphi](https://github.com/donnyphi)).

---

## 📸 Demo

> _Add a screenshot or GIF here after running the app locally (e.g. `docs/home.png`)._

```
[ Home ] [ Right-Hand Rule ] [ Field Around a Wire ] [ Charged Particle Motion ] [ Practice Mode ]
```

---

## What it does

Magnetism Lab is a small interactive textbook for the magnetism unit of an
introductory E&M course. It has five pages:

- **Home** — a landing page laying out the learning path and why magnetism is hard.
- **Right-Hand Rule Trainer** — predict and check the direction of `F = q(v × B)`
  on a labeled 3D vector plot, with a worked examples table.
- **Magnetic Field Around a Wire** — circular field lines, dot/cross (⊙/⊗)
  notation, and a distance-scaling experiment showing the `1/r` falloff.
- **Charged Particle Motion** — radius, force, period, and angular frequency of a
  charge orbiting in a uniform field, plus a side-by-side compare mode.
- **Practice Mode** — 20+ questions across five topics with hints, scoring,
  streaks, and a personalized "what to review next" summary.

## Why I built it

I'm a first-year physics + AI student, and magnetism was the unit where the gap
between *the equations* and *what's actually happening in space* felt the widest.
Cross products, invisible fields, and circular motion are all much easier to
understand when you can grab a slider and watch them change. I wanted a tool that
made that intuition the default — so I built one and used it to study.

## Why this matters

E&M is hard for reasons that have little to do with algebra:

- You have to **reason in 3D** — velocity, field, and force all point in different
  directions, which a flat textbook page struggles to show.
- **Fields are invisible**, so it's easy to lose track of where they point and how
  strong they are.
- **Cross products are unintuitive** — `v × B` points perpendicular to *both*
  inputs, which takes real practice to picture.
- The **sign of the charge flips everything**, often in surprising ways.

Magnetism Lab bridges that gap by making each of these visible, interactive, and
testable, so equations connect to motion you can actually see.

## Features

- 🖐️ Right-hand-rule trainer with a **predict-first mode** and a labeled 3D plot
- 🧲 Wire-field visualizer with **⊙/⊗ notation** and a `1/r` distance experiment
- 🌀 Charged-particle simulator with **compare mode** (e.g. doubled B vs. current)
- 🎯 Practice mode: **23 questions**, 5 topics, difficulty labels, two-tier hints,
  numeric answers checked with tolerance, score/streak/accuracy, and a session
  summary that recommends a review module
- 🎨 Custom card-based UI (hero, formula cards, intuition checks) on top of Streamlit
- ✅ Pure, tested physics functions (38 unit tests)

## Physics concepts covered

- Lorentz force and the magnetic force on a moving charge, `F = q(v × B)`
- Cross products and direction rules
- Magnetic field around a long straight wire, `B = μ₀I / (2πr)`
- Circular motion in a uniform magnetic field, `r = mv / (|q|B)`
- Cyclotron period and angular frequency, `T = 2πm / (|q|B)`, `ω = |q|B / m`
- How charge sign reverses the direction of motion

## Tech stack

- **Python 3.10+**
- **Streamlit** — UI and interactivity
- **NumPy** — vector math
- **Matplotlib** — 3D and 2D plots
- **pytest** — physics unit tests

## Project structure

```
magnetism-lab/
├── app.py                  # Streamlit entry point + sidebar navigation
├── modules/                # One file per page
│   ├── home.py
│   ├── right_hand_rule.py
│   ├── wire_field.py
│   ├── charged_particle.py
│   └── practice.py         # quiz engine + question bank
├── utils/
│   ├── physics.py          # pure, tested physics formulas (single source of truth)
│   ├── plotting.py         # Matplotlib figure helpers
│   └── ui.py               # reusable HTML/CSS components (hero, cards, ...)
└── tests/
    └── test_physics.py
```

## Installation

```bash
git clone https://github.com/donnyphi/magnetism-lab.git
cd magnetism-lab
pip install -r requirements.txt
```

## Run it locally

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually <http://localhost:8501>).

## Run the tests

```bash
python -m pytest -q
```

## Example modules

- **Right-Hand Rule Trainer** — choose a charge sign, a velocity, and a field;
  guess the force direction; reveal whether you were right.
- **Field Around a Wire** — set the current and direction; watch the field lines
  and see B at `r`, `2r`, and `3r` side by side.
- **Charged Particle Motion** — tune mass, speed, charge, and field; compare the
  orbit against a doubled-field version.

## What I learned

- How to keep physics logic **pure and testable** by isolating it from the UI, so
  the quiz and the simulations literally share the same formulas.
- Designing a **card-based UI** on top of Streamlit with custom HTML/CSS while
  keeping the page code readable.
- Turning equations into **legible visualizations** (consistent colors, labeled
  axes, direction arrows) that teach rather than just decorate.
- Writing a small **quiz engine** with session state, streaks, and per-topic
  analytics.

## Future improvements

- A full **electric field** module
- **Electromagnetic induction** (Faraday's law) simulations
- A **solenoid / current-loop** visualizer
- **User accounts** and saved progress
- Automatic **problem generation** with randomized values
- Public deployment on **Streamlit Community Cloud**

## License

Released under the MIT License — free to use and learn from.
