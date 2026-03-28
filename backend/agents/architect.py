from utils.llm import generate
import json

class Architect:
    def generate(self, persona):
        prompt = f"""
You are an AI roadmap generator.

Persona:
{persona}

Generate a STRICT JSON response ONLY.

Format:
{{
  "day_1_5": "...",
  "day_6_10": "...",
  "day_11_20": "...",
  "day_21_30": "...",
  "hidden_gem": "..."
}}

No explanation. Only JSON.
"""
        response = generate(prompt)

        try:
            return json.loads(response)
        except:
            return {
                "error": "Invalid JSON from LLM",
                "raw": response
            }