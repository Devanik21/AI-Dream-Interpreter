import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import uuid
import datetime
import random
import json
import time
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Must be FIRST Streamlit command
st.set_page_config(page_title="DreamsWhisperer", layout="centered", page_icon="🌒")

with st.sidebar:
    st.image("dream1.jpg", caption="🪞 Astral Mirror", use_container_width=True)



st.image("dream4.jpg",use_container_width=True)
# Optional: Add a toggle in the sidebar to enable/disable background music
# In Sidebar
with st.sidebar:
    st.markdown("## 🎼 Dream Soundscape")
    play_music = st.checkbox("Enable ambient music", value=True)

# Near the top of the app, after st.set_page_config and CSS
if play_music:
    st.audio("inner_peace.mp3", format="audio/mp3")



# --- Load the CSS from the original app ---
st.markdown("""
<style>


.glow-orb {
  position: fixed;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.1), transparent 70%);
  width: 120px;
  height: 120px;
  animation: pulseGlow 6s ease-in-out infinite;
  z-index: -2;
}

@keyframes pulseGlow {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.5); opacity: 0.2; }
}

@keyframes floatStars {
  from { transform: translateY(0); opacity: 0.2; }
  to { transform: translateY(-100vh); opacity: 0; }
}

.star {
  position: fixed;
  width: 2px;
  height: 2px;
  background: #ffffff80;
  animation: floatStars 10s linear infinite;
}

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

.tarot-card {
    transition: transform 0.6s ease, box-shadow 0.6s ease;
    cursor: pointer;
    max-width: 150px;
    border-radius: 10px;
    box-shadow: 0 0 15px #1a052e;
}

.tarot-card:hover {
    transform: translateY(-10px) scale(1.05);
    box-shadow: 0 0 25px #43256b;
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

.tab-content {
    padding: 20px;
    background: linear-gradient(145deg, #0a0217, #0c041a);
    border-radius: 0 0 15px 15px;
    box-shadow: 0 0 15px #1a052e inset;
    border: 1px solid #25083d;
    border-top: none;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #0c041a !important;
    border: 1px solid #25083d !important;
    border-radius: 15px 15px 0 0 !important;
    color: #886aab !important;
    padding: 10px 16px !important;
    height: 45px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, #25083d, #13052a) !important;
    color: #9a71c1 !important;
    border-bottom: none !important;
    box-shadow: 0 0 10px #1a052e;
}

.dream-stat {
    background: linear-gradient(145deg, #0c041a, #13052a);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    color: #9a71c1;
    border: 1px solid #25083d;
    box-shadow: 0 0 10px #1a052e inset;
}

.dream-stat h3 {
    margin-top: 0;
    font-size: 1.2em;
}

.dream-stat p {
    font-size: 2em;
    margin: 5px 0;
    color: #7348aa;
}

.mood-tag {
    background: linear-gradient(90deg, #25083d, #31104a);
    color: #9a71c1;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 0.8em;
    margin: 5px;
    display: inline-block;
    box-shadow: 0 0 8px #1a052e;
}

.mood-tag:hover {
    background: linear-gradient(90deg, #31104a, #43256b);
    box-shadow: 0 0 12px #43256b;
    transform: scale(1.05);
}

/* Custom lunar phase slider */
.lunar-slider .stSlider {
    padding-top: 45px !important;
    padding-bottom: 20px !important;
}

.lunar-slider [data-baseweb="slider"] {
    background: linear-gradient(90deg, #0c021b00, #321456, #0c021b00) !important;
    height: 4px !important;
}

.lunar-slider [data-baseweb="thumb"] {
    width: 30px !important;
    height: 30px !important;
    background: radial-gradient(#9a71c1, #43256b) !important;
    box-shadow: 0 0 10px #7348aa !important;
    border: none !important;
    top: -13px !important;
}

.lunar-slider [data-baseweb="track"] {
    height: 8px !important;
    background: linear-gradient(90deg, #25083d, #43256b) !important;
    border-radius: 4px !important;
}

/* Dream Visualization */
.dream-viz {
    border-radius: 15px;
    box-shadow: 0 0 20px #43256b;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='glow-orb' style='top: 20%; left: 10%; animation-delay: 0s;'></div>
<div class='glow-orb' style='top: 60%; left: 80%; animation-delay: 2s;'></div>
<div class='glow-orb' style='top: 40%; left: 50%; animation-delay: 4s;'></div>
""", unsafe_allow_html=True)


st.markdown("""
<div class='star' style='left: 20%; animation-delay: 0s;'></div>
<div class='star' style='left: 40%; animation-delay: 2s;'></div>
<div class='star' style='left: 60%; animation-delay: 4s;'></div>
<div class='star' style='left: 80%; animation-delay: 6s;'></div>
""", unsafe_allow_html=True)

# --- Initialize Session State Variables ---
if "dream_log" not in st.session_state:
    st.session_state.dream_log = []
if "saved_emotions" not in st.session_state:
    st.session_state.saved_emotions = {}
if "lucidity_score" not in st.session_state:
    st.session_state.lucidity_score = 1
if "moon_phase" not in st.session_state:
    st.session_state.moon_phase = ""
if "daily_streak" not in st.session_state:
    st.session_state.daily_streak = 0
if "last_entry_date" not in st.session_state:
    st.session_state.last_entry_date = None
if "tarot_cards" not in st.session_state:
    st.session_state.tarot_cards = []
if "dreams_by_day" not in st.session_state:
    st.session_state.dreams_by_day = {
        "Monday": 0, "Tuesday": 0, "Wednesday": 0, 
        "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0
    }
if "dream_themes" not in st.session_state:
    st.session_state.dream_themes = {}
if "spiritual_insights_unlocked" not in st.session_state:
    st.session_state.spiritual_insights_unlocked = []

# --- FEATURE 1: Lunar Calendar & Moon Phase Generator ---
def get_current_moon_phase():
    # Simple algorithm to generate a moon phase for storytelling purposes
    moon_phases = [
        "🌑 New Moon - Seeds of Subconscious", 
        "🌒 Waxing Crescent - Rising Shadow",
        "🌓 First Quarter - Inner Conflict", 
        "🌔 Waxing Gibbous - Approaching Insight",
        "🌕 Full Moon - Complete Awareness", 
        "🌖 Waning Gibbous - Fading Illusions",
        "🌗 Last Quarter - Integration", 
        "🌘 Waning Crescent - Final Surrender"
    ]
    today = datetime.datetime.now()
    # Use day of year to cycle through moon phases (simplified)
    phase_index = (today.timetuple().tm_yday % len(moon_phases))
    return moon_phases[phase_index]

# --- FEATURE 2: Dream Art Generator ---
def generate_dream_art(dream_text, mood):
    # Create a simple abstract visualization based on dream text
    width, height = 400, 300
    
    # Create base canvas with gradient background
    img = Image.new('RGB', (width, height), color=(10, 2, 25))
    draw = ImageDraw.Draw(img)
    
    # Set mood color
    if "fear" in mood.lower() or "nightmare" in mood.lower():
        color_scheme = [(80, 10, 80), (130, 0, 20), (80, 0, 40)]
    elif "peaceful" in mood.lower() or "calm" in mood.lower():
        color_scheme = [(30, 40, 100), (20, 80, 120), (40, 60, 100)]
    elif "mystical" in mood.lower() or "spiritual" in mood.lower():
        color_scheme = [(80, 40, 120), (120, 70, 150), (60, 30, 100)]
    else:
        color_scheme = [(67, 20, 110), (90, 40, 140), (50, 20, 80)]
    
    # Create abstract shapes based on dream text length
    seed = sum(ord(c) for c in dream_text[:20])
    random.seed(seed)
    
    # Generate nebulous clouds
    for _ in range(15):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(20, 100)
        color = random.choice(color_scheme)
        for i in range(size, 0, -2):
            alpha = int(100 * i/size)
            r, g, b = color
            fill_color = (r, g, b, alpha)
            draw.ellipse((x-i, y-i, x+i, y+i), fill=fill_color)
            
    # Add some "stars"
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(150, 250)
        draw.ellipse((x-size, y-size, x+size, y+size), fill=(brightness, brightness, brightness))
    
    # Apply blur
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Convert to base64 for embedding
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- FEATURE 3: Dream Pattern Analysis ---
def analyze_dream_patterns():
    if len(st.session_state.dream_log) < 2:
        return "Need more dreams to analyze patterns."
        
    themes = {}
    for dream, _ in st.session_state.dream_log:
        words = dream.lower().split()
        for theme in ["water", "falling", "flying", "chase", "teeth", "death", "lost"]:
            if theme in words:
                themes[theme] = themes.get(theme, 0) + 1
    
    st.session_state.dream_themes = themes
    
    if not themes:
        return "No common dream themes detected yet."
    
    top_theme = max(themes.items(), key=lambda x: x[1])
    
    interpretation = {
        "water": "You're processing emotions or the unconscious mind.",
        "falling": "You may be feeling insecure or loss of control in waking life.",
        "flying": "You're seeking freedom or transcendence.",
        "chase": "You may be avoiding a threatening situation in waking life.",
        "teeth": "Anxiety about appearance or communication issues.",
        "death": "You're experiencing transformation or endings.",
        "lost": "You may feel directionless or searching for purpose."
    }
    
    return f"Recurring theme: {top_theme[0].title()} ({top_theme[1]} occurrences) - {interpretation.get(top_theme[0], '')}"

# --- FEATURE 4: Tarot Integration ---
def draw_tarot_cards():
    major_arcana = [
        ("The Fool", "New beginnings, innocence, spontaneity"),
        ("The Magician", "Manifestation, resourcefulness, power"),
        ("The High Priestess", "Intuition, unconscious, inner voice"),
        ("The Empress", "Nurturing, abundance, fertility"),
        ("The Emperor", "Authority, structure, leadership"),
        ("The Hierophant", "Tradition, conformity, spiritual wisdom"),
        ("The Lovers", "Choices, relationships, harmony"),
        ("The Chariot", "Determination, control, victory"),
        ("Strength", "Courage, inner strength, resilience"),
        ("The Hermit", "Soul-searching, introspection, guidance"),
        ("Wheel of Fortune", "Change, cycles, destiny"),
        ("Justice", "Fairness, truth, law"),
        ("The Hanged Man", "Surrender, letting go, new perspective"),
        ("Death", "Endings, change, transformation"),
        ("Temperance", "Balance, moderation, harmony"),
        ("The Devil", "Shadow self, attachment, materialism"),
        ("The Tower", "Sudden change, revelation, upheaval"),
        ("The Star", "Hope, inspiration, spirituality"),
        ("The Moon", "Illusion, fear, subconscious"),
        ("The Sun", "Success, joy, vitality"),
        ("Judgment", "Reflection, reckoning, awakening"),
        ("The World", "Completion, accomplishment, fulfillment")
    ]
    
    # Draw three random cards
    st.session_state.tarot_cards = random.sample(major_arcana, 3)
    
    return st.session_state.tarot_cards

# --- FEATURE 5: Dream Dictionary ---
def get_dream_symbol_meaning(symbol):
    dream_dictionary = {
        "water": "Represents emotions, the unconscious, and life's flow",
        "fire": "Symbolizes transformation, passion, and destruction or rebirth",
        "flying": "Indicates freedom, transcendence, or escaping limitations",
        "falling": "Suggests insecurity, loss of control, or letting go",
        "teeth": "Connected to appearance, communication, or power",
        "snake": "Represents transformation, healing, or hidden fears",
        "house": "Symbolizes the self, personality, and your inner spaces",
        "death": "Indicates transformation, endings, and new beginnings",
        "baby": "Symbolizes new beginnings, vulnerability, or a neglected aspect of self",
        "money": "Represents self-worth, energy exchange, or values",
        "mirror": "Indicates self-reflection, identity, and truth perception",
        "door": "Symbolizes opportunities, transitions, and choices",
        "forest": "Represents the unknown, unconscious, or feeling lost",
        "ocean": "Symbolizes the collective unconscious, emotions, or overwhelm",
        "animals": "Often represents instinctual aspects of self or personality traits",
        "chase": "Indicates avoidance, fear, or unresolved conflicts",
        "naked": "Suggests vulnerability, authenticity, or fear of exposure",
        "exam": "Represents self-evaluation, fear of failure, or feeling tested"
    }
    
    return dream_dictionary.get(symbol.lower(), "Symbol not found in dream dictionary.")

# --- FEATURE 6: Daily Streak Counter ---
def update_dream_streak():
    today = datetime.date.today()
    
    # Update day of week counter
    day_name = today.strftime("%A")
    st.session_state.dreams_by_day[day_name] += 1
    
    # Update streak logic
    if st.session_state.last_entry_date is None:
        st.session_state.daily_streak = 1
    elif st.session_state.last_entry_date == today - datetime.timedelta(days=1):
        st.session_state.daily_streak += 1
    elif st.session_state.last_entry_date < today:
        st.session_state.daily_streak = 1
        
    st.session_state.last_entry_date = today

# --- FEATURE 7: Spiritual Insight System ---
def unlock_spiritual_insight():
    insights = [
        "🌌 Shadow Integration: Your darkness holds your greatest teacher.",
        "🪞 Mirror Principle: Others reflect aspects of your unconscious.",
        "🕸️ Dream Web: All dreams connect to a single cosmic tapestry.",
        "🌀 Spiral Evolution: You revisit the same themes at higher levels.",
        "🧿 Third Eye Activation: Dreams are messages from your higher self.",
        "🔮 Akashic Record: Dreams access universal knowledge beyond time.",
        "🪐 Planetary Influence: Celestial bodies affect dream symbolism.",
        "🧙 Dream Alchemy: Transmuting shadow elements into spiritual gold.",
        "🪄 Conscious Dreaming: Awakening within the dream state.",
        "🔥 Phoenix Rebirth: Death symbols announce spiritual awakening."
    ]
    
    if len(st.session_state.dream_log) % 3 == 0:
        # Unlock insight every 3 dreams
        available_insights = [i for i in insights if i not in st.session_state.spiritual_insights_unlocked]
        if available_insights:
            new_insight = random.choice(available_insights)
            st.session_state.spiritual_insights_unlocked.append(new_insight)
            return new_insight
    return None

# --- FEATURE 8: Dream Mood Tracking ---
def extract_emotions(interpretation):
    # Simple emotion extraction from interpretation text
    emotions = []
    emotion_keywords = {
        "fear": ["fear", "afraid", "terror", "dread", "horror", "anxious"],
        "joy": ["joy", "happiness", "delight", "pleasure", "bliss", "ecstasy"],
        "sadness": ["sad", "sorrow", "grief", "melancholy", "despair"],
        "anger": ["anger", "rage", "fury", "wrath", "hostility", "irritation"],
        "confusion": ["confusion", "bewilderment", "perplexity", "uncertainty"],
        "peace": ["peace", "calm", "tranquility", "serenity", "harmony"],
        "anticipation": ["anticipation", "expectation", "excitement", "hope"],
        "disgust": ["disgust", "revulsion", "distaste", "aversion"],
        "surprise": ["surprise", "astonishment", "amazement", "shock"],
        "trust": ["trust", "confidence", "reliance", "faith"],
        "mystical": ["mystical", "spiritual", "transcendent", "divine", "cosmic"]
    }
    
    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            if keyword in interpretation.lower():
                emotions.append(emotion)
                break
    
    # Return at least one emotion
    if not emotions:
        emotions = ["mystical"]  # Default emotion
    
    return list(set(emotions))  # Remove duplicates

# --- FEATURE 9: Lucidity Score Calculator ---
def calculate_lucidity_score(dream_text):
    lucidity_indicators = [
        "realize", "aware", "conscious", "control", "lucid", 
        "flying", "change", "manipulate", "decided to", "knew i was dreaming"
    ]
    
    score = 1  # Base score
    
    dream_lower = dream_text.lower()
    for indicator in lucidity_indicators:
        if indicator in dream_lower:
            score += 1
    
    return min(10, score)  # Max score of 10

# --- FEATURE 10: Dream Visualization Chart ---
def generate_dream_stats_chart():
    if len(st.session_state.dream_log) < 1:
        return None
    
    # Prepare data for visualization
    days = list(st.session_state.dreams_by_day.keys())
    counts = list(st.session_state.dreams_by_day.values())
    
    # Create dream frequency chart
    plt.figure(figsize=(8, 4))
    plt.style.use('dark_background')
    
    # Set colors
    plt.rcParams['text.color'] = '#9a71c1'
    plt.rcParams['axes.labelcolor'] = '#9a71c1'
    plt.rcParams['xtick.color'] = '#9a71c1'
    plt.rcParams['ytick.color'] = '#9a71c1'
    plt.rcParams['axes.edgecolor'] = '#503080'
    plt.rcParams['axes.facecolor'] = '#0c041a'
    plt.rcParams['figure.facecolor'] = '#0c041a'
    
    # Create bar chart
    bars = plt.bar(days, counts, color='#503080')
    
    # Add gradient effect to bars
    for i, bar in enumerate(bars):
        bar_height = bar.get_height()
        bar.set_color('#43256b')
        bar.set_edgecolor('#7348aa')
        bar.set_linewidth(1)
        
    plt.title('Dream Journal Entries by Day', color='#9a71c1')
    plt.ylabel('Number of Dreams')
    plt.tight_layout()
    
    # Convert plot to image
    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.getvalue()).decode()

# --- Title and Welcome Section ---
st.title("✨🌙 DreamsWhisperer: Mystic Visions Unveiled")

# Display current moon phase at the top
st.session_state.moon_phase = get_current_moon_phase()
st.markdown(f"""
<div style='
    background: linear-gradient(145deg, #2d0e4e, #1a082f, #2d0e4e);
    padding: 1.5rem;
    border-radius: 18px;
    box-shadow: 0 0 25px #5e2e91, 0 0 40px #37005f inset;
    border: 1px solid #8b52d730;
    color: #f5e8ff;
    font-size: 1.1rem;
    line-height: 1.7;
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
    text-align: center;
'>
<div style="position: relative; z-index: 1;">
<span style="font-size: 1.3em;">{st.session_state.moon_phase}</span>
</div>
</div>
""", unsafe_allow_html=True)

# Introduction text
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

# --- Sidebar: App Controls ---
with st.sidebar:
    st.markdown("## 🌑 Access the Void")
    api_key = st.text_input("🔮 Enter your Gemini API Key", type="password")
    
    # Show streak in sidebar
    if st.session_state.daily_streak > 0:
        st.markdown(f"""
        <div class="dream-stat">
            <h3>✨ Dream Streak</h3>
            <p>{st.session_state.daily_streak}</p>
            <span>consecutive days</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Display unlocked insights
    if st.session_state.spiritual_insights_unlocked:
        st.markdown("### 🧿 Spiritual Insights")
        for insight in st.session_state.spiritual_insights_unlocked:
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #0a0217, #130525);
                border: 1px solid #25083d;
                border-radius: 12px;
                padding: 12px;
                margin-bottom: 10px;
                font-size: 0.9em;
                color: #9a71c1;
            ">
            {insight}
            </div>
            """, unsafe_allow_html=True)
    
    # Clear dream log button
    if st.session_state.dream_log:
        if st.button("🗑️ Clear Dream Log"):
            st.session_state.dream_log = []
            st.session_state.saved_emotions = {}
            st.session_state.dream_themes = {}
            st.experimental_rerun()

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    
    # --- Create tabs for different features ---
    tab1, tab2, tab3, tab4 = st.tabs(["🌙 Dream Journal", "🔮 Tarot Reading", "📊 Dream Stats", "📖 Dream Dictionary"])
    
    with tab1:
        st.markdown("## 🪐 Your Shadow Vision")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.text_input("🌒 Your Age", placeholder="e.g. 21")
            if age and not age.isdigit():
                st.warning("⚠️ Age must be numeric.")
                st.stop()
                
        with col2:
            gender = st.selectbox("🌌 Your Inner Nature", 
                                ["Select", "Masculine", "Feminine", "Non-binary", "Void", "Fluid", "Other"])
        
        # Lucidity slider
        st.markdown("<div class='lunar-slider'>", unsafe_allow_html=True)
        lucidity = st.slider("🧿 Dream Lucidity Level", 1, 10, 1, 
                            help="How aware were you that you were dreaming? (1 = Not at all, 10 = Fully lucid)")
        st.markdown("</div>", unsafe_allow_html=True)
        
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

                    # Calculate lucidity score and update streak
                    st.session_state.lucidity_score = calculate_lucidity_score(dream)
                    update_dream_streak()
                    
                    # Check for new spiritual insight
                    new_insight = unlock_spiritual_insight()
                    
                    prompt = f"""
You are NocturneVisions, a mysterious and cryptic dream interpreter. Use Jungian archetypes, shadow psychology, and occult symbolism to analyze the dream deeply.

Dreamer Info:
- Age: {age if age else 'Unknown'}
- Nature: {gender if gender != 'Select' else 'Unspecified'}
- Current Moon Phase: {st.session_state.moon_phase}
- Lucidity Level: {lucidity}/10

Nocturnal Vision:
\"\"\"{dream}\"\"\"

Respond as an ancient oracle from the void. Include:
1. Shadow symbolism and dark archetypes (personal and collective unconscious) 🌑
2. Psychological undercurrents and repressed elements 🪞
3. Transformative potential and soul evolution 🌌
4. Core emotions present in the dream state
5. At least one significant dream symbol with detailed meaning

Tone: dark, cryptic, profound, mysterious, hypnotic.
"""

                    response = model.generate_content(prompt)
                    interpretation = response.text

                    # Extract emotions from interpretation
                    emotions = extract_emotions(interpretation)
                    st.session_state.saved_emotions[len(st.session_state.dream_log)] = emotions
                    
                    # Generate dream art
                    primary_mood = emotions[0] if emotions else "mystical"
                    dream_art_b64 = generate_dream_art(dream, primary_mood)
                    
                    # Save the dream entry
                    st.session_state.dream_log.append((dream, interpretation))
                    
                    # Display interpretation
                    st.markdown("### 🌌 Shadows Interpreted")
                    st.markdown(f"<div class='dream-box'>{interpretation}</div>", unsafe_allow_html=True)
                    
                    # Display dream art
                    st.markdown("### 🎨 Dream Vision Materialized")
                    st.markdown(f"""
                    <div style='text-align: center;'>
                        <img src='data:image/png;base64,{dream_art_b64}' class='dream-viz'>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display emotions
                    st.markdown("### 🌊 Emotional Currents")
                    st.markdown("<div style='margin: 10px 0;'>", unsafe_allow_html=True)
                    for emotion in emotions:
                        st.markdown(f"<span class='mood-tag'>{emotion.title()}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Show lucidity score
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(145deg, #25083d, #43256b);
                        padding: 15px;
                        border-radius: 12px;
                        text-align: center;
                        margin: 20px 0;
                    '>
                    <p style='margin: 0;'>🧿 Lucidity Score: {st.session_state.lucidity_score}/10</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show new spiritual insight if unlocked
                    if new_insight:
                        st.markdown(f"""
                        <div style='
                            background: linear-gradient(145deg, #43256b, #7348aa);
                            padding: 20px;
                            border-radius: 15px;
                            text-align: center;
                            margin: 25px 0;
                            box-shadow: 0 0 25px #43256b;
                            animation: pulse 2s infinite;
                        '>
                        <h3 style='margin-top: 0;'>🌟 New Insight Unlocked!</h3>
                        <p style='font-size: 1.1em;'>{new_insight}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Generate audio
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

    with tab2:
        st.markdown("## 🔮 Tarot Guidance")
        st.markdown("""
        <div class="dream-box">
        The ancient cards align with your dream energies, revealing hidden patterns and potential futures.
        Draw three cards from the Major Arcana to illuminate your dream's deeper meaning.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🃏 Draw Cards"):
            st.session_state.tarot_cards = draw_tarot_cards()
            
        if st.session_state.tarot_cards:
            st.markdown("### Your Spread")
            
            positions = ["Past Shadows", "Present Reality", "Future Potential"]
            
            cols = st.columns(3)
            for i, ((card, meaning), position) in enumerate(zip(st.session_state.tarot_cards, positions)):
                with cols[i]:
                    st.markdown(f"""
                    <div style='text-align: center;'>
                        <div style='
                            background: linear-gradient(145deg, #25083d, #13052a);
                            border: 2px solid #503080;
                            border-radius: 15px;
                            padding: 20px 10px;
                            min-height: 200px;
                            box-shadow: 0 0 20px #1a052e;
                            margin-bottom: 10px;
                        '>
                            <h3 style='margin-top: 0'>{card}</h3>
                            <p style='font-size: 0.9em; margin-bottom: 5px; color: #7348aa;'>{position}</p>
                            <hr style='width: 50%; margin: 10px auto;'>
                            <p style='font-size: 0.8em;'>{meaning}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Generate tarot insight for latest dream if available
            if st.session_state.dream_log:
                latest_dream = st.session_state.dream_log[-1][0]
                cards_text = ", ".join([card for card, _ in st.session_state.tarot_cards])
                
                st.markdown("### 🔮 Tarot Dream Connection")
                
                with st.spinner("Consulting the astral realm..."):
                    tarot_prompt = f"""
You are an enigmatic tarot reader with deep knowledge of dream symbolism and shadow psychology.

The dreamer has had this dream:
\"\"\"{latest_dream}\"\"\"

And drew these three tarot cards: {cards_text}

Provide a short mystical interpretation (2-3 paragraphs) that connects the dream symbols with the tarot cards.
Focus on revealing hidden truths and potential growth paths.
Use a poetic, cryptic tone with cosmic and occult imagery.
"""
                    tarot_response = model.generate_content(tarot_prompt)
                    tarot_interpretation = tarot_response.text
                    
                    st.markdown(f"<div class='dream-box'>{tarot_interpretation}</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("## 📊 Dream Pattern Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            # Dream count stat
            st.markdown(f"""
            <div class="dream-stat">
                <h3>🌙 Dreams Recorded</h3>
                <p>{len(st.session_state.dream_log)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Average lucidity score
            avg_lucidity = st.session_state.lucidity_score if len(st.session_state.dream_log) == 1 else 1
            st.markdown(f"""
            <div class="dream-stat">
                <h3>🧿 Lucidity Level</h3>
                <p>{avg_lucidity}/10</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Dream frequency chart
        chart_b64 = generate_dream_stats_chart()
        if chart_b64:
            st.markdown("### 📈 Dream Frequency")
            st.markdown(f"""
            <div style='text-align: center; margin: 20px 0;'>
                <img src='data:image/png;base64,{chart_b64}' class='dream-viz'>
            </div>
            """, unsafe_allow_html=True)
        
        # Pattern analysis
        if len(st.session_state.dream_log) > 0:
            pattern_insight = analyze_dream_patterns()
            st.markdown("### 🧩 Dream Patterns")
            st.markdown(f"<div class='dream-box'>{pattern_insight}</div>", unsafe_allow_html=True)
            
            # Display emotion stats if available
            if st.session_state.saved_emotions:
                # Count emotions
                all_emotions = []
                for emotions in st.session_state.saved_emotions.values():
                    all_emotions.extend(emotions)
                
                emotion_counts = {}
                for emotion in all_emotions:
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                
                if emotion_counts:
                    st.markdown("### 🌊 Emotional Landscape")
                    emotion_cols = st.columns(len(emotion_counts))
                    
                    for i, (emotion, count) in enumerate(emotion_counts.items()):
                        with emotion_cols[i]:
                            st.markdown(f"""
                            <div class="dream-stat">
                                <h3>{emotion.title()}</h3>
                                <p>{count}</p>
                                <span>dreams</span>
                            </div>
                            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("## 📖 Dream Dictionary")
        st.markdown("""
        <div class="dream-box">
        Seek wisdom from the ancient lexicon of dream symbols. Enter a symbol to unveil its hidden meaning
        across cultures and psychological traditions.
        </div>
        """, unsafe_allow_html=True)
        
        dream_symbol = st.text_input("🔍 Enter a dream symbol", placeholder="e.g. water, snake, falling")
        
        if dream_symbol:
            meaning = get_dream_symbol_meaning(dream_symbol.strip())
            st.markdown(f"""
            <div class="dream-box">
                <h3 style="margin-top: 0;">{dream_symbol.title()}</h3>
                <hr>
                {meaning}
            </div>
            """, unsafe_allow_html=True)
            
            # Generate expanded interpretation if not found in basic dictionary
            if "not found" in meaning:
                with st.spinner("Consulting ancient texts..."):
                    symbol_prompt = f"""
You are DreamOracle, keeper of ancient dream wisdom.
Provide a detailed symbolic interpretation (1-2 paragraphs) of the symbol: {dream_symbol}
Include:
1. Common psychological interpretations across cultures
2. Shadow aspects of this symbol
3. Potential transformative meaning

Use a mystical, poetic tone but remain informative.
"""
                    symbol_response = model.generate_content(symbol_prompt)
                    expanded_meaning = symbol_response.text
                    
                    st.markdown(f"""
                    <div class="dream-box">
                        <h3 style="margin-top: 0;">Expanded Interpretation</h3>
                        <hr>
                        {expanded_meaning}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Show common symbols from dream logs
        if st.session_state.dream_themes:
            st.markdown("### 🔍 Common Symbols in Your Dreams")
            themes_html = ""
            for theme, count in st.session_state.dream_themes.items():
                themes_html += f"<span class='mood-tag'>{theme.title()} ({count})</span> "
            
            st.markdown(f"<div style='margin: 15px 0;'>{themes_html}</div>", unsafe_allow_html=True)

    # --- Dream Journal with dark styling ---
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
                
                # Show emotions if available
                if (len(st.session_state.dream_log) - idx) in st.session_state.saved_emotions:
                    emotions = st.session_state.saved_emotions[len(st.session_state.dream_log) - idx]
                    emotions_html = ""
                    for emotion in emotions:
                        emotions_html += f"<span class='mood-tag'>{emotion.title()}</span> "
                    
                    st.markdown(f"<div style='margin: 10px 0;'>{emotions_html}</div>", unsafe_allow_html=True)

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



with st.sidebar:
    st.image("dream3.jpg", caption="🧿 Eye of the Inner Realms", use_container_width=True)

st.image("dream2.jpg" ,caption="🕯️ Gateway to the Void",use_container_width=True)
