import json
import re

def extract_json(text):
    # Remove markdown
    text = text.replace("```json", "").replace("```", "").strip()

    # Find the first JSON array
    start = text.find("[")
    end = text.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("No JSON array found.")

    json_text = text[start:end + 1]

    return json.loads(json_text)