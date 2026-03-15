# AI Dream Interpreter

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square) ![Stars](https://img.shields.io/github/stars/Devanik21/AI-Dream-Interpreter?style=flat-square&color=yellow) ![Forks](https://img.shields.io/github/forks/Devanik21/AI-Dream-Interpreter?style=flat-square&color=blue) ![Author](https://img.shields.io/badge/Author-Devanik21-black?style=flat-square&logo=github) ![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> Decode the language of dreams — AI-powered dream analysis using Jungian symbolism, psychological frameworks, and pattern recognition across your dream journal.

---

**Topics:** `conversational-ai` · `deep-learning` · `dream-analysis` · `generative-ai` · `large-language-models` · `natural-language-processing` · `nlp` · `psychology-ai` · `symbolic-interpretation` · `text-generation`

## Overview

AI Dream Interpreter is a psychological companion application that helps users explore the symbolic
content of their dreams through multiple interpretive lenses: Jungian analytical psychology (archetypes,
shadow, anima/animus, collective unconscious symbols), Freudian psychoanalytic theory (wish fulfilment,
symbolism), and contemporary cognitive dream research (memory consolidation, emotional processing,
problem-solving theories). Rather than presenting a single "correct" interpretation, the application
offers multiple frameworks and invites the dreamer to reflect on which resonates most personally.

Each dream entry is processed through a symbol extraction pipeline: named entities (people, places,
objects) are identified; emotional tone is classified; recurring symbols are matched against a curated
psychological symbol database; and the overall narrative structure (pursuit, flying, falling, loss)
is categorised. The LLM then synthesises these extracted elements into a multi-paragraph interpretive
reading that is personalised, nuanced, and psychologically grounded.

A longitudinal analysis module tracks dream themes, symbols, and emotional patterns across the
user's entire dream journal, identifying recurring archetypes, emotional cycles, and thematic clusters
that evolve over time. Monthly synthesis reports highlight dominant symbols, significant changes in
dream emotional tone, and potential connections between dream themes and recorded waking life events.

---

## Motivation

Dreams are one of the most intimate and enigmatic aspects of human experience. Whether one believes
dreams carry psychological meaning or are merely neurological noise, the practice of attending to
them — recording, reflecting, looking for patterns — is associated with increased self-awareness
and emotional processing. This project was built to make that practice richer and more systematic,
not to claim definitive psychological authority.

---

## Architecture

```
Dream Entry (narrative text + date + emotional note)
        │
  NLP Extraction:
  ├── Symbol identification (spaCy NER + custom symbol DB)
  ├── Emotional tone classification (NRC lexicon)
  └── Narrative structure classification (pursuit/flying/etc.)
        │
  LLM Interpretive Engine:
  ├── Jungian lens (archetypes, shadow, collective symbols)
  ├── Cognitive lens (memory/emotional processing theory)
  └── Personal lens (user's recurring themes)
        │
  Longitudinal Pattern Analysis (across all entries)
        │
  Streamlit: journal interface + analytics dashboard
```

---

## Features

### Multi-Framework Dream Analysis
Interpretations offered through three distinct psychological frameworks — Jungian, Freudian, and cognitive dream science — presented as complementary perspectives for the dreamer's own reflection.

### Symbol Extraction and Mapping
Automatic identification of significant symbols from the dream narrative, cross-referenced against a curated database of 500+ psychologically significant dream symbols with their traditional interpretations.

### Emotional Tone Classification
NRC emotion lexicon-based classification of the dream's emotional palette: joy, fear, anger, sadness, anticipation, trust, surprise, disgust — with relative intensity scores.

### Archetype Recognition
Identification of Jungian archetypal figures in dream characters: the Shadow, the Anima/Animus, the Wise Old Man/Woman, the Trickster, the Hero — with contextual interpretation.

### Longitudinal Symbol Tracking
Calendar heatmap and trend charts of recurring symbols, emotional tones, and archetypal figures across the full dream journal — revealing psychological patterns invisible entry-by-entry.

### Dream Lucidity Index
Optional tagging of lucid vs. non-lucid dreams with a trend chart of lucidity frequency over time, correlated with sleep quality and stress level notes.

### Monthly Synthesis Report
AI-generated monthly psychological synthesis: dominant themes, significant symbolic shifts, archetypal activity summary, and suggested areas for reflective journalling or waking attention.

### Private and Encrypted Storage
All dream entries stored in a locally encrypted SQLite database — never transmitted without explicit user consent.

---

## Tech Stack

| Library / Tool | Role | Why This Choice |
|---|---|---|
| **OpenAI GPT-4o / Gemini** | Interpretive analysis | Nuanced multi-framework dream interpretation |
| **spaCy** | Symbol extraction | NER for entities and custom symbol pattern matching |
| **NRC Emotion Lexicon** | Emotional analysis | Emotion word association scoring |
| **SQLite + encryption** | Private storage | Local encrypted dream journal database |
| **Streamlit** | Journal interface | Dream entry, symbol display, analytics |
| **Plotly** | Pattern visualisation | Symbol frequency charts, emotion heatmaps |
| **pandas** | Longitudinal analysis | Cross-entry pattern computation |

---

## Getting Started

### Prerequisites

- Python 3.9+ (or Node.js 18+ for TypeScript/JavaScript projects)
- A virtual environment manager (`venv`, `conda`, or equivalent)
- API keys as listed in the Configuration section

### Installation

```bash
git clone https://github.com/Devanik21/AI-Dream-Interpreter.git
cd AI-Dream-Interpreter
python -m venv venv && source venv/bin/activate
pip install streamlit openai spacy pandas plotly python-dotenv
python -m spacy download en_core_web_sm
echo 'OPENAI_API_KEY=sk-...' > .env
streamlit run app.py
```

---

## Usage

```bash
# Launch dream journal
streamlit run app.py

# Analyse a dream from CLI
python interpret.py --dream 'I was flying over a dark ocean...' --framework jungian

# Generate monthly synthesis
python monthly_report.py --month 2026-02

# Export dream journal
python export.py --format markdown --output dreams_archive.md
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | `(required)` | LLM API key for interpretive analysis |
| `PRIMARY_FRAMEWORK` | `jungian` | Default interpretive framework: jungian, cognitive, freudian |
| `SYMBOL_DB_PATH` | `data/symbols.json` | Path to dream symbol database |
| `LUCIDITY_TRACKING` | `True` | Enable lucid dream tagging and tracking |

> Copy `.env.example` to `.env` and populate required values before running.

---

## Project Structure

```
AI-Dream-Interpreter/
├── README.md
├── requirements.txt
├── app.py
└── ...
```

---

## Roadmap

- [ ] Sleep quality correlation: import sleep tracker data to correlate dream patterns with sleep stages
- [ ] Audio dream recording: voice-to-text transcription for recording dreams immediately upon waking
- [ ] Dream visualisation: AI image generation of key dream scenes from the narrative description
- [ ] Community symbol library: opt-in anonymous contribution of symbol frequencies across dreamers
- [ ] CBT-I integration: cognitive behavioural therapy for insomnia techniques informed by recurring nightmare patterns

---

## Contributing

Contributions, issues, and suggestions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Commit your changes: `git commit -m 'feat: add your idea'`
4. Push to your branch: `git push origin feature/your-idea`
5. Open a Pull Request with a clear description

Please follow conventional commit messages and add documentation for new features.

---

## Notes

Dream interpretation is not a diagnostic or therapeutic tool. This application provides symbolic and psychological frameworks for personal reflection, not clinical analysis. If you are experiencing distressing recurring nightmares or sleep disruption, please consult a qualified mental health professional.

---

## Author

**Devanik Debnath**  
B.Tech, Electronics & Communication Engineering  
National Institute of Technology Agartala

[![GitHub](https://img.shields.io/badge/GitHub-Devanik21-black?style=flat-square&logo=github)](https://github.com/Devanik21)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-devanik-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/devanik/)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with curiosity, depth, and care — because good projects deserve good documentation.*
