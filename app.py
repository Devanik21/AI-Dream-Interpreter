import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import uuid

# Must be FIRST Streamlit command
st.set_page_config(page_title="✨ DreamsWhisperer", layout="centered", page_icon="🔮")

# --- Enchanted Dreamscape CSS ---
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0a001a 0%, #16062d 50%, #1f0a40 100%);
    color: #e0c5ff;
    font-family: 'Georgia', serif;
    background-attachment: fixed;
}

h1, h2, h3 {
    background: linear-gradient(90deg, #c18fff, #f0c7ff, #a59aff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0px 0px 10px rgba(186, 104, 255, 0.5);
}

textarea, input, select {
    background: linear-gradient(145deg, #150428, #1d063a) !important;
    color: #f0dfff !important;
    border: 1px solid #743fbd !important;
    border-radius: 12px !important;
    box-shadow: inset 0 0 8px #4a0080 !important;
}

.stButton button {
    background: linear-gradient(90deg, #7e3db9, #9942e5) !important;
    color: #fff !important;
    border-radius: 15px;
    padding: 0.7em 1.4em;
    border: none;
    box-shadow: 0 0 15px #9152e0, 0 0 5px #ffffff60 inset;
    transition: all 0.4s ease;
}

.stButton button:hover {
    background: linear-gradient(90deg, #9942e5, #be7aff) !important;
    box-shadow: 0 0 20px #d193ff;
    transform: scale(1.05) translateY(-2px);
}

.dream-box {
    background: linear-gradient(145deg, #2b1a45, #1b0c2e);
    padding: 1.8rem;
    border-radius: 20px;
    box-shadow: 0 0 25px #37005f;
    margin-bottom: 1.5rem;
    color: #e5d0ff;
    border: 1px solid #743fbd40;
    position: relative;
    overflow: hidden;
}

.dream-box::before {
    content: "";
    position: absolute;
    top: -10px;
    left: -10px;
    right: -10px;
    bottom: -10px;
    background: linear-gradient(45deg, #7e3db930, #be7aff30, #2b1a4500);
    z-index: -1;
    filter: blur(20px);
    animation: aurora 8s infinite alternate;
}

@keyframes aurora {
    0% { transform: translateX(-10%) translateY(10%) rotate(0deg); opacity: 0.7; }
    50% { opacity: 0.3; }
    100% { transform: translateX(10%) translateY(-10%) rotate(180deg); opacity: 0.7; }
}

.spinner {
    font-size: 1.5em;
    color: #bb86fc;
    animation: pulse 1.2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.8; }
    50% { transform: scale(1.1); opacity: 1; }
}

hr {
    background: linear-gradient(90deg, #18042900, #743fbd50, #18042900);
    height: 2px;
    border: none;
}

a {
    color: #d4a1ff;
    text-decoration: none;
    transition: all 0.3s;
}

a:hover {
    color: #f0c7ff;
    text-shadow: 0 0 5px #a59aff;
}

/* Stars animation */
.stars {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    animation: twinkle var(--duration) infinite;
    opacity: 0;
}

@keyframes twinkle {
    0% { opacity: 0; }
    50% { opacity: var(--opacity); }
    100% { opacity: 0; }
}
</style>

<script>
function createStars() {
    const stars = document.createElement('div');
    stars.className = 'stars';
    document.body.appendChild(stars);
    
    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        const size = Math.random() * 3;
        
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.left = `${Math.random() * 100}%`;
        star.style.top = `${Math.random() * 100}%`;
        star.style.setProperty('--duration', `${5 + Math.random() * 10}s`);
        star.style.setProperty('--opacity', `${0.5 + Math.random() * 0.5}`);
        
        stars.appendChild(star);
    }
}

document.addEventListener('DOMContentLoaded', createStars);
</script>
""", unsafe_allow_html=True)

# --- Title ---
st.title("✨🌙 DreamsWhisperer: Mystic Visions Unveiled")

st.markdown("""
<div style='
    background: linear-gradient(145deg, #2d0e4e, #1a082f, #2d0e4e);
    padding: 1.8rem;
    border-radius: 18px;
    box-shadow: 0 0 25px #5e2e91, 0 0 40px #37005f inset;
    border: 1px solid #8b52d730;
    color: #f5e8ff;
    font-size: 1.1rem;
    line-height: 1.7;
    position: relative;
    overflow: hidden;
'>
<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
    background: radial-gradient(circle at 20% 50%, #8b52d715 0%, transparent 25%),
             radial-gradient(circle at 80% 30%, #c18fff10 0%, transparent 20%);
    z-index: 0;"></div>
<div style="position: relative; z-index: 1;">
✨🌠 <b>Greetings, dreamer of the cosmic tapestry...</b><br><br>
I am <b>DreamsWhisperer</b>, your ethereal guide through the luminous realms beyond waking.<br>
Share your nocturnal vision, and I shall unveil the sacred symbols hidden within your subconscious.
<br><br>
<span style="color:#d4afff;">🧙‍♀️ <i>For a deeper journey into your psyche, share your age and identity essence~</i></span>
</div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar: Gemini API Key ---
st.sidebar.markdown("## 🌠 Connect to the Ethereal Realm")
api_key = st.sidebar.text_input("🔮 Enter your Gemini API Key", type="password")

if "dream_log" not in st.session_state:
    st.session_state.dream_log = []

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    st.markdown("## 🌌 Your Ethereal Vision")
    age = st.text_input("🌟 Your Age", placeholder="e.g. 21")
    if age and not age.isdigit():
        st.warning("⚠️ Age must be numeric.")
        st.stop()

    gender = st.selectbox("🌈 Your Essence Identity", ["Select", "Male", "Female", "Non-binary", "Fluid", "Other"])
    dream = st.text_area("💫 Reveal Your Dream Vision...", 
                         placeholder="e.g. I floated through a cathedral of crystal flowers while cosmic whispers echoed...", 
                         height=180)

    if st.button("🔮 Unveil the Mystic Meaning"):
        if not dream.strip():
            st.warning("🌘 Paint your dream vision to unlock its secrets.")
        else:
            with st.spinner("Reading the astral patterns..."):
                st.markdown("<p class='spinner'>✨🌠💫 Traversing the veils of your subconscious...</p>", unsafe_allow_html=True)

                prompt = f"""
You are DreamsWhisperer, an ethereal and intuitive dream interpreter. Use Jungian archetypes, emotional symbolism, and mystical insights to analyze the dream deeply.

Dreamer Info:
- Age: {age if age else 'Unknown'}
- Identity: {gender if gender != 'Select' else 'Unspecified'}

Dream Vision:
\"\"\"{dream}\"\"\"

Respond as a mystical, wise oracle with poetic language. Include:
1. Symbolic meanings and archetypes (universal and personal) 🌌
2. Emotional resonances and psychological insights 🌊
3. Spiritual significance and transformative potential 🔮

Tone: ethereal, poetic, mystical, transcendent, wise.
"""

                response = model.generate_content(prompt)
                interpretation = response.text

                st.session_state.dream_log.append((dream, interpretation))

                st.markdown("### 🌠 Ethereal Insights Revealed")
                st.markdown(f"<div class='dream-box'>{interpretation}</div>", unsafe_allow_html=True)

                # Audio
                tts = gTTS(interpretation)
                audio_path = f"dream_audio_{uuid.uuid4()}.mp3"
                tts.save(audio_path)
                st.audio(audio_path, format="audio/mp3")
                st.download_button("🎵 Download Ethereal Whispers", open(audio_path, "rb"), file_name="dream_whispers.mp3")
                os.remove(audio_path)

                # Download Text
                st.download_button("📜 Download Sacred Text", data=interpretation, file_name="dream_revelation.txt")

    # Dream Journal
    if st.session_state.dream_log:
        st.markdown("## 📓 Your Astral Chronicles")
        for idx, (d, interp) in enumerate(reversed(st.session_state.dream_log), 1):
            with st.expander(f"✨ Vision #{len(st.session_state.dream_log) - idx + 1}"):
                st.markdown(f"<div class='dream-box'><b>🌙 Dream Vision:</b><br>{d}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='dream-box'><b>🔮 Mystic Revelation:</b><br>{interp}</div>", unsafe_allow_html=True)

        full_journal = "\n\n✧･ﾟ: *✧･ﾟ:* *:･ﾟ✧*:･ﾟ✧\n\n".join(
            [f"Dream Vision:\n{d}\n\nMystic Revelation:\n{i}" for d, i in st.session_state.dream_log]
        )
        st.download_button("🌠 Download Complete Astral Chronicles", data=full_journal, file_name="astral_chronicles.txt")

else:
    st.markdown("""
    <div class='dream-box' style='text-align: center;'>
    <span style='font-size: 1.3em; color: #a59aff;'>🌙✨</span><br>
    To begin your journey through the veils of dreams,<br>
    please provide your Gemini API key.
    </div>
    """, unsafe_allow_html=True)
