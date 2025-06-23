import streamlit as st
import random
import math
import qrcode
import io

# --------------------------
# Setup: Problem List
problems = [
    (18, 30), (45, 75), (105, 70), (24, 36),
    (91, 65), (84, 36), (40, 60), (21, 63),
    (128, 96), (14, 49)
]

# Shuffle once at session start
if "shuffled_problems" not in st.session_state:
    st.session_state.shuffled_problems = random.sample(problems, len(problems))
    st.session_state.index = 0
    st.session_state.score = 0

# --------------------------
# Suggest Method Hint
def suggest_method(a, b):
    diff = abs(a - b)
    smaller = min(a, b)
    larger = max(a, b)

    # Heuristic for suggesting method
    if smaller < 20 or larger < 50:
        return "Try using **Prime Factorization**."
    elif diff < 15:
        return "Hint: Try **Euclidean Subtraction** method."
    else:
        return "Hint: Use the **Euclidean Division** method."

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
if st.session_state.index < len(st.session_state.shuffled_problems):
    a, b = st.session_state.shuffled_problems[st.session_state.index]
    st.subheader(f"🔢 Problem {st.session_state.index + 1} of {len(st.session_state.shuffled_problems)}")
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
        del st.session_state.shuffled_problems
        del st.session_state.index
        del st.session_state.score
        st.rerun()
