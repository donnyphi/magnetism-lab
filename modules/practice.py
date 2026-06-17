import streamlit as st

QUESTIONS = [
    {"q":"Positive charge: v = +x, B = +y. Force?", "choices":["+z","-z","zero","+x"], "a":"+z", "hint":"Use x cross y.", "exp":"For positive charge, +x × +y = +z."},
    {"q":"Negative charge: v = +x, B = +y. Force?", "choices":["+z","-z","zero","+y"], "a":"-z", "hint":"Find positive answer, then reverse.", "exp":"Positive would be +z, so negative charge gives -z."},
    {"q":"If v is parallel to B, magnetic force is...", "choices":["maximum","zero","negative","infinite"], "a":"zero", "hint":"Cross product depends on sin(theta).", "exp":"When theta = 0, sin(theta)=0, so force is zero."},
    {"q":"Current out of the page gives field lines that are...", "choices":["clockwise","counterclockwise","straight up","zero"], "a":"counterclockwise", "hint":"Right thumb out of page.", "exp":"Curling fingers show counterclockwise field lines."},
    {"q":"For a wire, if distance r doubles, B becomes...", "choices":["twice as large","half as large","four times as large","unchanged"], "a":"half as large", "hint":"B is proportional to 1/r.", "exp":"B = μ₀I/(2πr), so doubling r halves B."},
    {"q":"Increasing magnetic field strength makes particle radius...", "choices":["larger","smaller","unchanged","infinite"], "a":"smaller", "hint":"r = mv/(|q|B).", "exp":"B is in the denominator, so stronger B means smaller radius."},
    {"q":"Increasing particle speed makes circular radius...", "choices":["larger","smaller","zero","unchanged"], "a":"larger", "hint":"r = mv/(|q|B).", "exp":"Speed is in the numerator, so radius grows."},
    {"q":"The magnetic force on a moving charge is always perpendicular to...", "choices":["velocity","mass","charge sign","time"], "a":"velocity", "hint":"Cross products create perpendicular vectors.", "exp":"q(v × B) is perpendicular to v and B."},
    {"q":"A larger mass in the same B field gives a particle path with...", "choices":["larger radius","smaller radius","no motion","same radius"], "a":"larger radius", "hint":"r = mv/(|q|B).", "exp":"Mass is in the numerator."},
    {"q":"Magnetic fields do work on charged particles in uniform circular motion?", "choices":["yes","no","only if positive","only if negative"], "a":"no", "hint":"Force is perpendicular to motion.", "exp":"A perpendicular force changes direction, not speed, so it does no work."},
]

def render():
    st.header("Practice Mode")
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = set()
    for i, item in enumerate(QUESTIONS, start=1):
        with st.expander(f"Question {i}: {item['q']}"):
            choice = st.radio("Choose one", item["choices"], key=f"q{i}")
            if st.button("Show hint", key=f"hint{i}"):
                st.info(item["hint"])
            if st.button("Submit", key=f"submit{i}"):
                if choice == item["a"]:
                    st.success("Correct. " + item["exp"])
                    if i not in st.session_state.answered:
                        st.session_state.score += 1
                        st.session_state.answered.add(i)
                else:
                    st.error(f"Not quite. Correct answer: {item['a']}. {item['exp']}")
    st.metric("Session score", f"{st.session_state.score} / {len(QUESTIONS)}")
