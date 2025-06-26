import streamlit as st
import random
import math
import qrcode
import io

# --------------------------
# Fixed Problem Set by Method
problems = [
    # Prime Factorization
    (18, 30), (24, 36), (40, 60),

    # Euclidean Subtraction
    (21, 63), (14, 49), (84, 36),

    # Euclidean Division
    (105, 70), (128, 96), (91, 65),

    # Any Method
    (45, 75)
]

# --------------------------
# Session State Initialization (no shuffle)
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0

# --------------------------
# Suggest Method Hint
def suggest_method(a, b):
    idx = st.session_state.index
    if idx <= 2:
        return "Try using **Prime Factorization**."
    elif idx <= 5:
        return "Hint: Try **Euclidean Subtraction** method."
    elif idx <= 8:
        return "Hint: Use the **Euclidean Division** method."
    else:
        return "Use **any method** you like."

# --------------------------
# Header
st.title("💡 GCD Lab")
st.markdown("Type the GCD of the number pair shown. Get instant feedback and move to the next!")

# Sidebar with QR code
st.sidebar.header("Scan This QR Code to View Menu Online")

qr_link = "https://gcd-lab.streamlit.app"
qr = qrcode.make(qr_link)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)

st.sidebar.image(buf, width=300, caption=qr_link)

# --------------------------
# Problem Display
if st.session_state.index < len(problems):
    a, b = problems[st.session_state.index]
    st.subheader(f"🔢 Problem {st.session_state.index + 1} of {len(problems)}")
    st.write(f"What is the GCD of **{a} and {b}**?")

    st.info(suggest_method(a, b))  # 👈 Hint display

    user_answer = st.number_input("Your answer:", min_value=1, step=1, key="input")

    if st.button("Submit"):
        correct = math.gcd(a, b)
        if user_answer == correct:
            st.success("✅ Correct!")
            st.session_state.score += 1
            st.session_state.index += 1
            st.rerun()
        else:
            st.error("❌ Incorrect. Try again!")

else:
    st.success("🎉 You've completed all problems!")
    st.write(f"Your score: **{st.session_state.score} / {len(problems)}**")

    if st.button("🔁 Start Over"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.rerun()
