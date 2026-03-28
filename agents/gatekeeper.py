from agents.profiler import Profiler
from agents.librarian import Librarian
from agents.architect import Architect
from utils.llm import generate

from services.memory import (
    save_message,
    get_messages,
    save_persona,
    get_persona
)

class Gatekeeper:
    def __init__(self):
        self.profiler = Profiler()
        self.librarian = Librarian()
        self.architect = Architect()
        self.user_id = 1  # simple single-user system

    def handle_chat(self, message):
        # save user message
        save_message(self.user_id, "user", message)

        # get history
        history = get_messages(self.user_id)

        # get persona
        persona = get_persona(self.user_id)

        resources = self.librarian.search(message)

        prompt = f"""
User persona: {persona}

Conversation history:
{history}

User message:
{message}

Relevant ET tools:
{resources}

Give helpful answer and recommend best resources.
"""

        reply = generate(prompt)

        # save AI reply
        save_message(self.user_id, "assistant", reply)

        return {
            "reply": reply,
            "resources": resources
        }

    def handle_voice(self, file):
        persona = self.profiler.process(file)

        save_persona(self.user_id, persona)

        return persona

    def get_roadmap(self):
        persona = get_persona(self.user_id)

        if not persona:
            persona = {"type": "student", "risk": "low", "goal": "learning"}

        return self.architect.generate(persona)