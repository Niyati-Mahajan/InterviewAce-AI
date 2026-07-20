import os
import joblib

# -----------------------------
# Load Model and Vectorizer
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "interview_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    print("✅ ML Model Loaded Successfully")

except Exception as e:
    print("❌ Error Loading ML Model:", e)

    model = None
    vectorizer = None


# -----------------------------
# Predict Student Answer
# -----------------------------

def predict_answer(student_answer):

    if model is None or vectorizer is None:
        return {
            "prediction": "Unknown",
            "confidence": 0
        }

    try:

        # Convert text into TF-IDF features
        text_vector = vectorizer.transform([student_answer])

        # Predict label directly
        prediction = model.predict(text_vector)[0]

        # Predict confidence
        if hasattr(model, "predict_proba"):

            confidence = max(model.predict_proba(text_vector)[0]) * 100

        else:

            confidence = 100

        return {
            "prediction": str(prediction),
            "confidence": round(float(confidence), 2)
        }

    except Exception as e:

        print("Prediction Error:", e)

        return {
            "prediction": "Unknown",
            "confidence": 0
        }