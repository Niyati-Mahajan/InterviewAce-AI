import json
import os

QUESTION_FOLDER = "dataset/questions"

def load_questions(subject_file):
    path = os.path.join(QUESTION_FOLDER, subject_file)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_questions(subject_file, questions):
    path = os.path.join(QUESTION_FOLDER, subject_file)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print("Question Manager Ready!")