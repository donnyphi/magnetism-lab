# Magnetism Lab

Magnetism Lab is a custom physics-simulator interface for freshman-level electricity and magnetism. Streamlit is used only as the deployment shell; the visible product is a vanilla HTML, CSS, and JavaScript app with animated canvas simulations.

I built this as a freshman MIT Physics + AI student project because magnetism is hard to learn from static diagrams. The direction rules are three-dimensional, the fields are invisible, and the equations only start to make sense once you can see what changes when you tune one variable at a time.

## What It Does

- Trains right-hand-rule intuition with animated vector visuals for `F = q(v x B)`
- Shows circular magnetic field lines around a current-carrying wire
- Animates charged particle motion in a uniform magnetic field
- Updates custom sliders, numeric readouts, and field animations in real time
- Runs a one-question-at-a-time practice trainer with score, streak, hints, explanations, and missed-question review
- Keeps Python physics utilities and tests for correctness while the UI runs as a custom web app

## Physics Covered

- Cross products and magnetic force direction
- Positive and negative charge behavior
- Magnetic fields around long straight wires
- `B = mu0 I / (2 pi r)` proportional reasoning
- Circular charged-particle motion
- `r = mv / |q|B`, `F = |q|vB`, and `T = 2 pi m / |q|B`
- Why magnetic fields do no work on a charged particle

## Screenshots

Add screenshots here after deployment:

- Home hero with orbit animation
- Right-Hand Rule vector visualizer
- Wire field simulator
- Charged particle orbit simulator
- Practice trainer

## Installation

```bash
cd magnetism-lab
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Tests

```bash
cd magnetism-lab
pytest
```

## Project Structure

```text
magnetism-lab/
  app.py              # Streamlit shell that renders the custom app component
  custom_app.html     # Full custom HTML/CSS/JS physics simulator
  utils/
    physics.py        # Tested Python physics helpers
  tests/
    test_physics.py
  README.md
  requirements.txt
```

## Future Improvements

- Add helical motion when velocity has a component parallel to `B`
- Add a free-rotation 3D vector trainer
- Add saved practice history and adaptive question selection
- Add challenge modes for AP Physics C and MIT 8.02-style problems
- Deploy publicly with polished screenshots and walkthrough notes

The goal is simple: make magnetism feel less like memorized hand motions and more like a physical system you can see, tune, and reason about.
