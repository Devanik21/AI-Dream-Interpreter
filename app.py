import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import uuid
import time

# --- Dreamy CSS ---
st.markdown("""
<style>
body {
    background-color: #f5f3ff;
    color: #4b0082;
    font-family: 'Comic Sans MS', cursive, sans-serif;
}

h1 {
    color: #8e44ad;
    text-align: center;
}

textarea, input, select {
    background-color: #ffffffdd !important;
    border-radius: 10px !important;
}

.block-container {
    padding: 2rem;
}

.dream-box {
    background: linear-gradient(145deg, #e0c3fc, #8ec5fc);
    padding: 1.5rem;
    border-radius: 20px;
    box-shadow: 0 0 10px #d3bfff;
}

.spinner {
    font-size: 1.2em;
    color: #7f00ff;
    animation: blink 1.2s infinite;
}

@keyframes blink {
  0%   { opacity: 0.2; }
  50%  { opacity: 1.0; }
  100% { opacity: 0.2; }
}
</style>
""", unsafe_allow_html=True)

# --- App Config ---
st.set_page_config(page_title="🌙 DreamyBot – Dream Interpreter", layout="centered", page_icon="💤")
st.title("💤🌙 **DreamyBot** – Your Magical Dream Interpreter ✨")

st.markdown("""
<div class='dream-box'>
Hi sweet soul~ I’m **DreamyBot** 🧚‍♀️  
Tell me your dream, and I’ll uncover the hidden meanings within it.  
I'll look deep into your subconscious with love and symbolic wisdom. 🌌💖

> 📝 *Include your age and gender for more intuitive reflections!*
</div>
""", unsafe_allow_html=True)

# --- Sidebar for API Key ---
st.sidebar.markdown("## 🔐 Gemini API Key")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# --- Dream Log ---
if "dream_log" not in st.session_state:
    st.session_state.dream_log = []

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    with st.container():
        st.markdown("### 🧸 Dream Details")
        age = st.text_input("🧑‍🎓 Your Age", placeholder="e.g. 19")
        if age and not age.isdigit():
            st.warning("Please enter a valid numeric age.")
            st.stop()
        gender = st.selectbox("🚻 Your Gender", ["Select", "Male", "Female", "Other"])
        dream = st.text_area("💭 What did you dream?", placeholder="e.g. A glowing doorway appeared in the sky...", height=180)

    if st.button("🔮 Interpret My Dream"):
        if not dream.strip():
            st.warning("Please describe your dream.")
        else:
            with st.spinner("✨ DreamyBot is gazing into the stars..."):
                st.markdown("<p class='spinner'>🌟✨ Looking through dreamdust...</p>", unsafe_allow_html=True)

                prompt = f"""
You are DreamyBot, a magical AI dream analyst who speaks with empathy and mystical insight.
Analyze this dream using Jungian and symbolic psychology.

Dreamer:
- Age: {age if age else 'unknown'}
- Gender: {gender if gender != 'Select' else 'unspecified'}

Dream:
\"\"\"{dream}\"\"\"

Provide:
1. A symbolic interpretation 🧠
2. Emotional themes 💞
3. Reflections or life insights 🔮

Tone: nurturing, poetic, intuitive, mystical.
"""

                response = model.generate_content(prompt)
                interpretation = response.text

                st.session_state.dream_log.append((dream, interpretation))

                st.markdown("### 🧠 DreamyBot Whispers:")
                st.markdown(f"<div class='dream-box'>{interpretation}</div>", unsafe_allow_html=True)

                # --- Text to Speech ---
                tts = gTTS(interpretation)
                audio_file = f"dream_audio_{uuid.uuid4()}.mp3"
                tts.save(audio_file)

                st.audio(audio_file, format="audio/mp3")
                st.download_button("🔊 Download Interpretation Audio", data=open(audio_file, "rb"), file_name="dream_interpretation.mp3")
                time.sleep(1)
                os.remove(audio_file)

                st.download_button("📝 Save as Text", data=interpretation, file_name="dream_interpretation.txt")

    # --- Dream Journal ---
    if st.session_state.dream_log:
        st.markdown("### 📖 Your Dream Journal (This Session)")
        for idx, (d, interp) in enumerate(reversed(st.session_state.dream_log), 1):
            with st.expander(f"🌠 Dream #{len(st.session_state.dream_log) - idx + 1}"):
                st.markdown(f"**💭 Dream:**\n{d}")
                st.markdown(f"**🔮 Interpretation:**\n{interp}")

        # Full Journal Download
        full_log = "\n\n---\n\n".join(
            [f"Dream:\n{d}\n\nInterpretation:\n{i}" for d, i in st.session_state.dream_log]
        )
        st.download_button("📘 Download Full Dream Journal", data=full_log, file_name="dream_journal.txt")

    else:
        st.info("📝 No dreams yet~ your magical journal will appear here 🌙")

else:
    st.warning("🌟 Please enter your Gemini API key in the sidebar to begin your dreamy journey.")

