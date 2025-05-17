# app.py
import streamlit as st
import google.generativeai as genai

# --- App Setup ---
st.set_page_config(page_title="DreamScope: AI Dream Interpreter", layout="centered")
st.title("🌙 DreamScope – AI Dream Interpreter")

st.markdown("""
Describe your dream, and let Gemini interpret its possible meanings, emotions, and symbols.
""")

# --- Sidebar ---
st.sidebar.title("🔐 Gemini API Key")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

visualize = st.sidebar.checkbox("🖼️ Generate Dream Visual (coming soon)", value=False)

# --- Main Logic ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    dream = st.text_area("🛌 Describe Your Dream", placeholder="I was flying through a forest chased by a shadow...", height=200)

    if st.button("Interpret Dream") and dream.strip():
        with st.spinner("Analyzing your dream with AI 🧠..."):
            prompt = f"""
You are an expert dream analyst.

Interpret the following dream:
\"\"\"{dream}\"\"\"

Provide:
1. A symbolic and psychological interpretation
2. The dominant emotions in the dream
3. Possible meanings or real-life connections
4. Archetypes or recurring dream motifs (e.g. flying, falling, shadows)

Be insightful yet imaginative.
"""

            response = model.generate_content(prompt)
            st.subheader("🌌 Dream Interpretation")
            st.markdown(response.text)

        if visualize:
            st.info("🔧 Dream visualization coming soon! (Image API placeholder)")
    else:
        st.info("Enter a dream and click interpret.")
else:
    st.warning("Please input your Gemini API key in the sidebar.")

