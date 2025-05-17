# app.py
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import uuid

# --- App Config ---
st.set_page_config(page_title="DreamyBot – Your Dream Interpreter", layout="centered")
st.title("🌙 DreamyBot")
st.markdown("""
Hi, I'm **DreamyBot** ✨  
Share your dream with me, and I’ll help interpret its symbols and emotions.

> 📝 *Tip: Include your age and gender for deeper insights!*
""")

# --- Sidebar for API Key ---
st.sidebar.title("🔐 Gemini API Key")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# Session log
if "dream_log" not in st.session_state:
    st.session_state.dream_log = []

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
                interpretation = response.text

                # Store dream & interpretation in session log
                st.session_state.dream_log.append((dream, interpretation))

                st.markdown("### 🧠 DreamyBot Says:")
                st.markdown(interpretation)

                # --- Text to Speech ---
                tts = gTTS(interpretation)
                audio_file = f"dream_audio_{uuid.uuid4()}.mp3"
                tts.save(audio_file)

                st.audio(audio_file, format="audio/mp3")
                st.download_button("🔊 Download Audio", data=open(audio_file, "rb"), file_name="dream_interpretation.mp3")

                # --- Download as Text ---
                st.download_button("📝 Download Interpretation", data=interpretation, file_name="dream_interpretation.txt")

                # Auto-scroll to result
                st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)

    # --- Show Session Log ---
    if st.session_state.dream_log:
        st.markdown("---")
        st.markdown("### 📘 Dream Journal (This Session)")
        for idx, (d, interp) in enumerate(reversed(st.session_state.dream_log), 1):
            with st.expander(f"Dream #{len(st.session_state.dream_log) - idx + 1}"):
                st.markdown(f"**Dream:** {d}")
                st.markdown(f"**Interpretation:** {interp}")

else:
    st.warning("Please enter your Gemini API key in the sidebar.")
