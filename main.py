"""
Mental Wellness Support Agent
Track: Agents for Good (Kaggle x Google 5-Day AI Agents Intensive)

This script implements a simple multi-agent system:
- Controller Agent
- Mood Analyzer Agent
- Coping Strategy Agent
- Motivation Agent

NOTE:
- Do NOT put your API key directly in this file.
- Set it as an environment variable: GEMINI_API_KEY
"""

import os
import datetime
from typing import List, Dict

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "google-generativeai is not installed. "
        "Install it with: pip install google-generativeai"
    )

# --------- LLM SETUP ----------

API_KEY_ENV_VAR = "GEMINI_API_KEY"

if API_KEY_ENV_VAR not in os.environ:
    raise EnvironmentError(
        f"Please set your Gemini API key in the environment variable {API_KEY_ENV_VAR} "
        "(do NOT hardcode keys in the code)."
    )

genai.configure(api_key=os.environ[API_KEY_ENV_VAR])

MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


def call_llm(system_prompt: str, user_message: str) -> str:
    """
    Helper to call the LLM with a system-style prompt + user message.
    """
    prompt = f"{system_prompt}\n\nUser message: {user_message}"
    response = model.generate_content(prompt)
    return response.text.strip()


# --------- AGENT DEFINITIONS ----------

def mood_analyzer_agent(user_message: str) -> str:
    """
    Agent 1: Analyze the user's emotional state.
    Output: short label like 'stressed', 'sad', 'okay', 'happy', etc.
    """
    system_prompt = (
        "You are a Mood Analyzer Agent. "
        "Read the user's message and return ONLY one or two words "
        "that describe their emotional state. Examples: "
        "'stressed', 'sad', 'anxious', 'overwhelmed', 'tired', 'okay', 'happy', "
        "'excited', 'confused'.\n"
        "Do not give sentences, only the mood label."
    )
    mood = call_llm(system_prompt, user_message)
    # Clean up – keep just first word usually
    return mood.split()[0].lower()


def coping_strategy_agent(user_message: str, mood: str) -> str:
    """
    Agent 2: Suggest practical coping strategies based on mood.
    """
    system_prompt = (
        "You are a Coping Strategy Agent helping a young student with mental wellness.\n"
        "User mood: " + mood + "\n\n"
        "Goals:\n"
        "- Suggest 3–5 short, practical, safe activities.\n"
        "- Focus on simple things like breathing exercises, journaling, short walk, "
        "mindfulness, talking to a friend, etc.\n"
        "- Use warm, encouraging tone.\n"
        "- Avoid giving medical or clinical advice. "
        "If the message sounds like severe depression, self-harm, or crisis, "
        "gently encourage them to reach out to a trusted adult or professional.\n"
    )
    return call_llm(system_prompt, user_message)


def motivation_agent(mood: str) -> str:
    """
    Agent 3: Give a short motivational message + affirmation.
    """
    system_prompt = (
        "You are a Motivation Agent. "
        "Based on the user's mood, share a short encouraging message "
        "and one positive affirmation.\n"
        "Mood: " + mood + "\n\n"
        "Format:\n"
        "- 2–3 sentences of encouragement.\n"
        "- Then on a new line, start with 'Affirmation: ' and give one sentence."
    )
    return call_llm(system_prompt, f"The user is feeling {mood}.")


# --------- CONTROLLER + MEMORY ----------

class WellnessMemory:
    """
    Simple in-memory store of user mood over time.
    For the competition writeup, we can describe this as 'short-term memory'.
    """

    def __init__(self):
        self.entries: List[Dict] = []

    def add_entry(self, mood: str, user_message: str):
        self.entries.append(
            {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "mood": mood,
                "message": user_message,
            }
        )

    def last_moods(self, n: int = 5) -> List[str]:
        return [e["mood"] for e in self.entries[-n:]]


class ControllerAgent:
    """
    Main Orchestrator:
    - Receives user input
    - Calls Mood Analyzer
    - Calls Coping Strategy + Motivation agents
    - Combines everything into a friendly response
    """

    def __init__(self):
        self.memory = WellnessMemory()

    def handle_message(self, user_message: str) -> str:
        # 1) Analyze mood
        mood = mood_analyzer_agent(user_message)
        self.memory.add_entry(mood, user_message)

        # 2) Get coping strategies
        coping_text = coping_strategy_agent(user_message, mood)

        # 3) Get motivational message
        motivation_text = motivation_agent(mood)

        # 4) Build combined response
        history_hint = ""
        last_moods = self.memory.last_moods()
        if len(last_moods) > 1:
            history_hint = (
                f"\n\n📈 Recent mood trend (last {len(last_moods)} messages): "
                + ", ".join(last_moods)
            )

        response = (
            f"🧠 I sense you might be feeling **{mood}** right now.\n\n"
            f"Here are some gentle suggestions you can try:\n\n"
            f"{coping_text}\n\n"
            f"{motivation_text}"
            f"{history_hint}\n\n"
            "⚠️ Note: I’m an AI support tool, not a professional. "
            "If you ever feel in danger or deeply hopeless, please talk to a trusted "
            "adult, friend, or mental health professional."
        )

        return response


# --------- SIMPLE CLI CHAT LOOP ----------

def main():
    print("🌿 Mental Wellness Support Agent")
    print("Type 'exit' to quit.\n")

    controller = ControllerAgent()

    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"exit", "quit"}:
            print("Agent: Sending you a big virtual hug. Take care 💛")
            break

        reply = controller.handle_message(user_message)
        print("\nAgent:\n" + reply + "\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
