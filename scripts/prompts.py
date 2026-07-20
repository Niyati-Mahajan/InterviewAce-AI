QUESTION_PROMPT = """
You are an expert technical interviewer.

Generate exactly 5 interview questions for the given subject and topic.

Return ONLY valid JSON.

Format:

[
  {
    "question": "...",
    "ideal_answer": "...",
    "difficulty": "Easy"
  }
]

Rules:

1. Return only JSON.
2. No markdown.
3. No explanation.
4. Difficulty must be Easy, Medium or Hard.
5. Ideal answer should be 50-120 words.
6. Questions should be suitable for technical interviews.
"""