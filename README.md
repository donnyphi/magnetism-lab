# Magnetism Lab

Interactive E&M simulations for magnetic fields, right-hand rules, and charged particle motion.

## Why I built it

I built Magnetism Lab as a freshman-level physics education tool to make electricity and magnetism more visual and intuitive. Magnetism is often hard because the ideas are three-dimensional: cross products, field directions, and circular motion are much easier to understand when you can manipulate them directly.

## Features

- Right-hand rule trainer for `F = q(v × B)`
- Magnetic field visualizer around a current-carrying wire
- Charged particle circular motion simulator
- Practice mode with hints and explanations
- Modular physics functions with tests

## Physics concepts covered

- Magnetic force on a moving charge
- Cross products and direction rules
- Magnetic field around a long straight wire
- Circular motion in a uniform magnetic field
- Cyclotron period
- Radius dependence on mass, speed, charge, and magnetic field

## Screenshots

_Add screenshots here after running the app locally._

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
python -m pytest
```

## Future improvements

- 3D Lorentz force visualizer
- Solenoid and current-loop modules
- Faraday's law and induction module
- Student progress tracking
- More generated practice problems
