import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import uuid

# Must be FIRST Streamlit command
st.set_page_config(page_title="🌑 DreamsWhisperer", layout="centered", page_icon="🌌")

# --- Advanced Dreamscape CSS ---
st.markdown("""
<style>
body {
    background: linear-gradient(125deg, #050013 0%, #0d0221 40%, #120429 100%);
    color: #9a71c1;
    font-family: 'Georgia', serif;
    background-attachment: fixed;
}

h1, h2, h3 {
    background: linear-gradient(90deg, #503080, #7348aa, #43256b);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0px 2px 15px rgba(82, 45, 128, 0.7);
}

textarea, input, select {
    background: linear-gradient(145deg, #0c021b, #13032c) !important;
    color: #9a71c1 !important;
    border: 1px solid #381a5c !important;
    border-radius: 12px !important;
    box-shadow: inset 0 0 12px #22083b !important;
    backdrop-filter: blur(5px) !important;
}

.stButton button {
    background: linear-gradient(90deg, #341855, #502680) !important;
    color: #9a71c1 !important;
    border-radius: 15px;
    padding: 0.7em 1.4em;
    border: none;
    box-shadow: 0 0 15px #2a0e45, 0 0 5px #3a1454 inset;
    transition: all 0.4s ease;
}

.stButton button:hover {
    background: linear-gradient(90deg, #43256b, #561d8f) !important;
    box-shadow: 0 0 20px #43256b;
    transform: scale(1.05) translateY(-2px);
}

.dream-box {
    background: linear-gradient(145deg, #140827, #0c041a);
    padding: 1.8rem;
    border-radius: 20px;
    box-shadow: 0 0 25px #1a052e;
    margin-bottom: 1.5rem;
    color: #886aab;
    border: 1px solid #321456;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(5px);
}

.dream-box::before {
    content: "";
    position: absolute;
    top: -10px;
    left: -10px;
    right: -10px;
    bottom: -10px;
    background: linear-gradient(45deg, #25083d30, #43125230, #13031d00);
    z-index: -1;
    filter: blur(20px);
    animation: aurora 12s infinite alternate;
}

@keyframes aurora {
    0% { transform: translateX(-10%) translateY(10%) rotate(0deg); opacity: 0.5; }
    50% { opacity: 0.2; }
    100% { transform: translateX(10%) translateY(-10%) rotate(180deg); opacity: 0.5; }
}

.spinner {
    font-size: 1.5em;
    color: #6c4298;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.6; }
    50% { transform: scale(1.1); opacity: 0.9; }
}

hr {
    background: linear-gradient(90deg, #0c021b00, #321456, #0c021b00);
    height: 2px;
    border: none;
}

a {
    color: #7348aa;
    text-decoration: none;
    transition: all 0.4s;
}

a:hover {
    color: #9a71c1;
    text-shadow: 0 0 8px #22083b;
}

/* Cosmic animations */
.cosmos {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    overflow: hidden;
}

.star {
    position: absolute;
    border-radius: 50%;
    animation: twinkle var(--duration) infinite;
    opacity: 0;
    background: radial-gradient(circle at center, var(--color) 0%, transparent 70%);
}

.nebula {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.04;
    animation: drift var(--drift-duration) infinite alternate ease-in-out;
}

.shooting-star {
    position: absolute;
    width: 2px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #43256b, transparent);
    filter: blur(1px);
    animation: shoot 4s linear infinite;
    opacity: 0;
    transform: rotate(var(--angle));
}

@keyframes twinkle {
    0% { opacity: 0; }
    50% { opacity: var(--opacity); }
    100% { opacity: 0; }
}

@keyframes drift {
    0% { transform: translate(0, 0); }
    100% { transform: translate(var(--drift-x), var(--drift-y)); }
}

@keyframes shoot {
    0% { transform: translateX(-100px) rotate(var(--angle)); opacity: 0; }
    5% { opacity: var(--opacity); }
    20% { transform: translateX(calc(100vw + 100px)) rotate(var(--angle)); opacity: 0; }
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
st.sidebar.markdown("## 🌑 Access the Void")
api_key = st.sidebar.text_input("🔮 Enter your Gemini API Key", type="password")

if "dream_log" not in st.session_state:
    st.session_state.dream_log = []

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    st.markdown("## 🪐 Your Shadow Vision")
    age = st.text_input("🌒 Your Age", placeholder="e.g. 21")
    if age and not age.isdigit():
        st.warning("⚠️ Age must be numeric.")
        st.stop()

    gender = st.selectbox("🌌 Your Inner Nature", ["Select", "Masculine", "Feminine", "Non-binary", "Void", "Fluid", "Other"])
    
    dream_container = st.container()
    with dream_container:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, #0a0217, #060110);
            border: 1px solid #25083d;
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 10px;
        ">
        <p style="color: #6c4298; margin-bottom: 5px;">🪞 Reveal Your Subconscious Shadows...</p>
        </div>
        """, unsafe_allow_html=True)
        
    dream = st.text_area("", 
                       placeholder="e.g. I descended an endless staircase as shadowy figures watched from doorways that opened into nothing...", 
                       height=180, key="dream_input")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        interpret_btn = st.button("🔮 Pierce the Veil")

    if interpret_btn:
        if not dream.strip():
            st.markdown("""
            <div style="
                background: linear-gradient(145deg, #0a0217, #130525);
                border: 1px solid #25083d;
                border-radius: 12px;
                padding: 15px;
                color: #503080;
                text-align: center;
                box-shadow: 0 0 15px #0c041a inset;
            ">
            ⚠️ Manifest your nightmare visions to unlock their secrets.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner(""):
                st.markdown("<p class='spinner'>🌑🪐⚫ Traversing the dark corridors of your unconscious...</p>", unsafe_allow_html=True)

                prompt = f"""
You are NocturneVisions, a mysterious and cryptic dream interpreter. Use Jungian archetypes, shadow psychology, and occult symbolism to analyze the dream deeply.

Dreamer Info:
- Age: {age if age else 'Unknown'}
- Nature: {gender if gender != 'Select' else 'Unspecified'}

Nocturnal Vision:
\"\"\"{dream}\"\"\"

Respond as an ancient oracle from the void. Include:
1. Shadow symbolism and dark archetypes (personal and collective unconscious) 🌑
2. Psychological undercurrents and repressed elements 🪞
3. Transformative potential and soul evolution 🌌

Tone: dark, cryptic, profound, mysterious, hypnotic.
"""

                response = model.generate_content(prompt)
                interpretation = response.text

                st.session_state.dream_log.append((dream, interpretation))

                st.markdown("### 🌌 Shadows Interpreted")
                st.markdown(f"<div class='dream-box'>{interpretation}</div>", unsafe_allow_html=True)

                # Audio with custom styling
                st.markdown("""
                <div style="
                    background: linear-gradient(145deg, #0a0217, #0c041a);
                    border: 1px solid #22083b;
                    border-radius: 12px;
                    padding: 15px;
                    margin-top: 10px;
                    margin-bottom: 20px;
                ">
                <p style="color: #503080; margin-bottom: 10px;">🔈 Void Whispers</p>
                """, unsafe_allow_html=True)
                
                tts = gTTS(interpretation)
                audio_path = f"vision_audio_{uuid.uuid4()}.mp3"
                tts.save(audio_path)
                st.audio(audio_path, format="audio/mp3")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("🎵 Download Void Whispers", open(audio_path, "rb"), file_name="void_whispers.mp3")
                with col2:
                    st.download_button("📜 Download Occult Text", data=interpretation, file_name="shadow_revelation.txt")
                
                st.markdown("</div>", unsafe_allow_html=True)
                os.remove(audio_path)

    # Dream Journal with dark styling
    if st.session_state.dream_log:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, #0c041a, #0a0217);
            border: 1px solid #25083d;
            border-radius: 12px;
            padding: 15px;
            margin-top: 30px;
            margin-bottom: 15px;
        ">
        <h2 style="color: #503080; margin-bottom: 10px; text-align: center;">📓 Shadow Chronicles</h2>
        </div>
        """, unsafe_allow_html=True)
        
        for idx, (d, interp) in enumerate(reversed(st.session_state.dream_log), 1):
            with st.expander(f"🌑 Vision #{len(st.session_state.dream_log) - idx + 1}"):
                st.markdown(f"<div class='dream-box'><b>🪐 Nightmare Vision:</b><br>{d}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='dream-box'><b>🌌 Occult Revelation:</b><br>{interp}</div>", unsafe_allow_html=True)

        full_journal = "\n\n⚫・☽・⚫・☾・⚫\n\n".join(
            [f"Nightmare Vision:\n{d}\n\nOccult Revelation:\n{i}" for d, i in st.session_state.dream_log]
        )
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.download_button("🌑 Download Complete Shadow Chronicles", data=full_journal, file_name="shadow_chronicles.txt")

else:
    st.markdown("""
    <div class='dream-box' style='text-align: center;'>
    <span style='font-size: 1.3em; color: #503080;'>🌑⚫</span><br>
    To enter the void between consciousness and dreams,<br>
    you must provide your Gemini API key.
    </div>
    """, unsafe_allow_html=True)
