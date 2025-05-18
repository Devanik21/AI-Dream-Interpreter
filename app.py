import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import uuid
import time

# Must be FIRST Streamlit command
st.set_page_config(page_title="🌙 DreamyBot – Dream Interpreter", layout="centered", page_icon="🔮")

# --- Dark Mystical CSS ---
st.markdown("""
<style>
body {
    background-color: #0d001f;
    color: #dcd2ff;
    font-family: 'Georgia', serif;
}

h1, h2, h3 {
    color: #f3e5ff;
    text-shadow: 1px 1px 4px #9c27b0;
}

textarea, input, select {
    background-color: #1a082f !important;
    color: #f0dfff !important;
    border: 1px solid #5e2e91 !important;
    border-radius: 10px !important;
}

.stButton button {
    background-color: #5e2e91 !important;
    color: #fff !important;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    border: none;
    box-shadow: 0 0 10px #ab47bc;
    transition: 0.3s ease;
}

.stButton button:hover {
    background-color: #7b42c7 !important;
    box-shadow: 0 0 15px #ce93d8;
}

.dream-box {
    background: linear-gradient(145deg, #2b1a45, #1b0c2e);
    padding: 1.5rem;
    border-radius: 20px;
    box-shadow: 0 0 20px #37005f;
    margin-bottom: 1rem;
    color: #e5d0ff;
}

.spinner {
    font-size: 1.2em;
    color: #bb86fc;
    animation: blink 1.2s infinite;
}

@keyframes blink {
  0%   { opacity: 0.2; }
  50%  { opacity: 1.0; }
  100% { opacity: 0.2; }
}

hr {
    border: 1px solid #37005f;
}

a {
    color: #d4a1ff;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🔮🌙 DreamyBot: Mystic Interpreter of Dreams")

st.markdown("""
<div class='dream-box'>
Welcome, seeker of secrets... 🕯️✨  
I am **DreamyBot**, your guide through the shadowy landscapes of dreams.  
Whisper your vision to me, and I shall reveal the hidden meanings that stir beneath.  
<br><br>
> 🦋 *For deeper insight, share your age and identity~*
</div>
""", unsafe_allow_html=True)

# --- Sidebar: Gemini API Key ---
st.sidebar.markdown("## 🧿 Connect to the Dream Realm")
api_key = st.sidebar.text_input("🔐 Enter your Gemini API Key", type="password")

if "dream_log" not in st.session_state:
    st.session_state.dream_log = []

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    st.markdown("## 🌌 Your Dream")
    age = st.text_input("🎭 Your Age", placeholder="e.g. 21")
    if age and not age.isdigit():
        st.warning("🌑 Age must be numeric.")
        st.stop()

    gender = st.selectbox("🌗 Your Gender Identity", ["Select", "Male", "Female", "Other"])
    dream = st.text_area("🌒 Tell Me Your Dream...", placeholder="e.g. I walked through a forest of mirrors under a violet sky...", height=180)

    if st.button("🔍 Reveal the Meaning"):
        if not dream.strip():
            st.warning("🌘 Describe your dream to unlock its secrets.")
        else:
            with st.spinner("🔮 Gazing into the dreammist..."):
                st.markdown("<p class='spinner'>🌟✨ Peering into your subconscious...</p>", unsafe_allow_html=True)

                prompt = f"""
You are DreamyBot, an intuitive and mysterious dream interpreter. Use Jungian archetypes and emotional symbolism to analyze the dream deeply.

Dreamer Info:
- Age: {age if age else 'Unknown'}
- Gender: {gender if gender != 'Select' else 'Unspecified'}

Dream:
\"\"\"{dream}\"\"\"

Respond like a poetic, wise oracle. Include:
1. Symbolic meaning and archetypes 🌌
2. Emotional undertones 🌊
3. Spiritual or personal reflections 🔮

Tone: dark, poetic, mystical, wise.
"""

                response = model.generate_content(prompt)
                interpretation = response.text

                st.session_state.dream_log.append((dream, interpretation))

                st.markdown("### 🌠 DreamyBot’s Reflection")
                st.markdown(f"<div class='dream-box'>{interpretation}</div>", unsafe_allow_html=True)

                # Audio
                tts = gTTS(interpretation)
                audio_path = f"dream_audio_{uuid.uuid4()}.mp3"
                tts.save(audio_path)
                st.audio(audio_path, format="audio/mp3")
                st.download_button("🎧 Download Audio", open(audio_path, "rb"), file_name="dream_interpretation.mp3")
                os.remove(audio_path)

                # Download Text
                st.download_button("📜 Download Text", data=interpretation, file_name="dream_interpretation.txt")

    # Dream Journal
    if st.session_state.dream_log:
        st.markdown("## 📓 Your Shadow Journal")
        for idx, (d, interp) in enumerate(reversed(st.session_state.dream_log), 1):
            with st.expander(f"🌙 Dream #{len(st.session_state.dream_log) - idx + 1}"):
                st.markdown(f"<div class='dream-box'><b>🌘 Dream:</b><br>{d}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='dream-box'><b>🔮 Interpretation:</b><br>{interp}</div>", unsafe_allow_html=True)

        full_journal = "\n\n---\n\n".join(
            [f"Dream:\n{d}\n\nInterpretation:\n{i}" for d, i in st.session_state.dream_log]
        )
        st.download_button("🗝️ Download Full Dream Journal", data=full_journal, file_name="full_dream_journal.txt")

else:
    st.warning("🧿 To enter the dream realm, please provide your Gemini API key.")
