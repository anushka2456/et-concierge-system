import requests

# ?? OpenRouter key (optional but recommended)
OPENROUTER_KEY = "PASTE_KEY_OR_LEAVE_EMPTY"

def cloud_llm(prompt):
    if not OPENROUTER_KEY:
        return None

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mixtral-8x7b-instruct",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

    except:
        return None


def local_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json().get("response", None)

    except:
        return None


def generate(prompt):
    # ?? Try cloud first
    result = cloud_llm(prompt)

    if result:
        return result

    # ?? fallback to local
    result = local_llm(prompt)

    if result:
        return result

    return "AI unavailable. Please try again."
