# mental-wellness-agent

**Track:** Agents for Good – Kaggle x Google 5-Day AI Agents Intensive Capstone Project  

This project is an AI agent that offers gentle emotional support, basic coping
strategies, and positive affirmations for students dealing with stress,
anxiety, or low motivation.

> ⚠️ Disclaimer: This agent is **not** a replacement for professional mental
> health care. In case of crisis, users should contact a trusted adult or
> professional.

---

## 1. Problem

Many students experience stress, anxiety, and overwhelm during their studies.
They often do not have someone available 24/7 to listen to them and suggest
healthy coping strategies. Small moments of support can make a big difference.

## 2. Solution

The **Mental Wellness Support Agent** provides:

- A warm, conversational AI that listens to the user.
- Mood analysis based on the user’s message.
- Context-aware coping suggestions (breathing, journaling, short breaks, etc.).
- Short motivational messages and affirmations.
- Simple mood history tracking to show trends over time.

---

## 3. Multi-Agent Architecture

The system is implemented as a **multi-agent** workflow:

1. **Controller Agent**
   - Orchestrates the whole flow.
   - Calls other agents and combines their outputs into a single response.

2. **Mood Analyzer Agent**
   - Reads the user’s message and predicts a mood label
     (e.g. `stressed`, `sad`, `tired`, `okay`, `happy`).

3. **Coping Strategy Agent**
   - Suggests 3–5 safe, practical activities the user can try.

4. **Motivation Agent**
   - Generates a short encouragement message and a positive affirmation.

5. **Wellness Memory**
   - Stores recent moods with timestamps.
   - Allows showing a simple “recent mood trend” to the user.

---

## 4. Technology

- **Language:** Python
- **LLM:** Gemini (`google-generativeai` Python SDK)
- **Model:** `gemini-1.5-flash`
- **Interface:** Simple command-line chat loop

No API keys are hard-coded in the repository.

---

## 5. How to Run (Locally)

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/mental-wellness-agent.git
cd mental-wellness-agent
