import whisper
import tempfile
from utils.llm import generate

class Profiler:
    def __init__(self):
        self.model = whisper.load_model("base")

    def process(self, file):
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(file.file.read())
            path = temp.name

        result = self.model.transcribe(path)
        text = result["text"]

        prompt = f"""
Extract user persona from this text:

{text}

Return JSON:
{{
  "type": "...",
  "risk": "...",
  "goal": "..."
}}
"""
        return generate(prompt)
