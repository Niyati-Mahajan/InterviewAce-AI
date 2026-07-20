import json
import os
import re
import joblib

from google import genai


# ==========================================================
# Load ML Model & Vectorizer
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "interview_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

svm_model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# ==========================================================
# ML Prediction
# ==========================================================

def predict_with_ml(question, student_answer):

    text = question + " " + student_answer

    vector = vectorizer.transform([text])

    predicted_label = svm_model.predict(vector)[0]

    score_map = {
        "Excellent": 10,
        "Good": 8,
        "Average": 6,
        "Poor": 3,
        "Very Poor": 1
    }

    predicted_score = score_map[predicted_label]

    return predicted_label, predicted_score


# ==========================================================
# Rule Based Fallback
# ==========================================================

def fallback_evaluation(question, ideal_answer, student_answer):

    label, score = predict_with_ml(question, student_answer)

    ideal_words = {
        word.lower()
        for word in re.findall(r"[A-Za-z0-9]+", ideal_answer)
    }

    student_words = {
        word.lower()
        for word in re.findall(r"[A-Za-z0-9]+", student_answer)
    }

    missing = sorted(list(ideal_words - student_words))[:5]

    return {
        "score": score,
        "predicted_label": label,
        "missing_concepts": missing,
        "correct_answer": ideal_answer,
        "suggestions": [
            "Explain the concept in more detail.",
            "Include one practical example.",
            "Use important technical keywords."
        ]
    }


# ==========================================================
# JSON Extractor
# ==========================================================

def extract_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found.")

    return json.loads(match.group())


# ==========================================================
# Main Evaluation Function
# ==========================================================

def evaluate_answer(
        api_key,
        model,
        question,
        ideal_answer,
        student_answer
):

    predicted_label, predicted_score = predict_with_ml(
        question,
        student_answer
    )

    # No Gemini API
    if not api_key:
        return fallback_evaluation(
            question,
            ideal_answer,
            student_answer
        )

    prompt = f"""
You are an experienced technical interviewer.

Evaluate the following interview answer.

Return ONLY valid JSON.

{{
"missing_concepts":[...],
"correct_answer":"...",
"suggestions":[...]
}}

Question:
{question}

Ideal Answer:
{ideal_answer}

Student Answer:
{student_answer}
"""

    try:

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        data = extract_json(response.text)

        return {

            "score": predicted_score,

            "predicted_label": predicted_label,

            "missing_concepts":
                data.get("missing_concepts", []),

            "correct_answer":
                data.get("correct_answer", ideal_answer),

            "suggestions":
                data.get("suggestions", [])

        }

    except Exception:

        return fallback_evaluation(
            question,
            ideal_answer,
            student_answer
        )


def fallback_interview_summary(question_reports):
    scores = [float(item.get("score", 0)) for item in question_reports]
    average_score = sum(scores) / len(scores) if scores else 0
    weak_topics = []

    for item in question_reports:
        weak_topics.extend(item.get("missing_concepts", []))

    readiness = (
        "Interview Ready"
        if average_score >= 8
        else "Nearly Ready"
        if average_score >= 6
        else "Needs More Practice"
    )

    return {
        "overall_rating": round(average_score, 1),
        "technical_skills": min(100, int(round(average_score * 10))),
        "communication": min(100, max(45, int(round(average_score * 9)))),
        "confidence": min(100, max(50, int(round(average_score * 9.5)))),
        "problem_solving": min(100, max(45, int(round(average_score * 8.8)))),
        "interview_readiness": readiness,
        "overall_suggestions": [
            "Add one practical example to each answer.",
            "Use more precise technical keywords.",
            "Practice concise answers under a timer."
        ],
        "overall_strengths": [
            "Completed the interview flow.",
            "Shows understanding of core concepts."
        ],
        "overall_weaknesses": weak_topics[:5] or ["Needs deeper explanation in a few answers."],
        "topics_to_revise": weak_topics[:5] or ["Core concepts from the selected subject."],
        "estimated_study_time": "3-5 hours",
        "practice_questions_recommendation": "Practice 10 mixed questions from weak topics.",
        "difficulty_recommendation": "Continue with the same difficulty, then move one level higher after scoring 8/10.",
        "learning_path": [
            "Revise weak concepts.",
            "Write short definitions.",
            "Practice examples.",
            "Attempt another timed mock interview."
        ],
        "final_recommendation": "Focus on weak topics and retake a 5-question mock interview."
    }


def evaluate_interview_summary(api_key, model, question_reports):
    """Ask Gemini for a complete interview-level evaluation with deterministic fallback."""
    if not api_key:
        return fallback_interview_summary(question_reports)

    prompt = f"""
You are a senior technical interviewer.

Evaluate this complete interview as one final report.

Return ONLY valid JSON with these keys:
{{
  "overall_rating": 0-10,
  "technical_skills": 0-100,
  "communication": 0-100,
  "confidence": 0-100,
  "problem_solving": 0-100,
  "interview_readiness": "...",
  "overall_suggestions": ["..."],
  "overall_strengths": ["..."],
  "overall_weaknesses": ["..."],
  "topics_to_revise": ["..."],
  "estimated_study_time": "...",
  "practice_questions_recommendation": "...",
  "difficulty_recommendation": "...",
  "learning_path": ["..."],
  "final_recommendation": "..."
}}

Interview Answers:
{json.dumps(question_reports, ensure_ascii=True)}
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model, contents=prompt)
        data = extract_json(response.text)
        fallback = fallback_interview_summary(question_reports)

        for key, value in fallback.items():
            data.setdefault(key, value)

        return data
    except Exception:
        return fallback_interview_summary(question_reports)
