# app.py
import streamlit as st
import google.generativeai as genai

# --- App Config ---
st.set_page_config(page_title="DreamyBot – Your Dream Interpreter", layout="centered")
st.title("🌙 DreamyBot")
st.markdown("""
Hi, I'm **DreamyBot** ✨  
Share your dream with me, and I’ll help interpret its symbols and emotions.

> 📝 *Tip: Include your age and gender for deeper insights!*
""")

# --- Sidebar API Key ---
st.sidebar.title("🔐 Gemini API Key")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    # --- User Inputs ---
    age = st.text_input("🧑‍🎓 Your Age", placeholder="e.g. 19")
    gender = st.selectbox("🚻 Your Gender", ["Select", "Male", "Female", "Other"])
    dream = st.text_area("💭 Describe Your Dream", placeholder="e.g. A princess was holding my hand, but her face was blank...", height=200)

    if st.button("Interpret My Dream"):
        if not dream.strip():
            st.warning("Please describe your dream.")
        else:
            with st.spinner("DreamyBot is thinking... ✨"):
                prompt = f"""
You are DreamyBot, an insightful AI dream analyst. Use Jungian and symbolic psychology to analyze the following dream.

Respond empathetically, almost like a therapist — explore archetypes, emotions, and themes. Use a warm, intuitive tone.

Dreamer details:
- Age: {age if age else 'unknown'}
- Gender: {gender if gender != 'Select' else 'unspecified'}

Dream:
\"\"\"{dream}\"\"\"

Provide:
1. A symbolic interpretation
2. Emotional themes
3. Reflections the user might consider
"""

                response = model.generate_content(prompt)
                st.markdown("### 🧠 DreamyBot:")
                st.markdown(response.text)
else:
    st.warning("Please enter your Gemini API key in the sidebar.")
