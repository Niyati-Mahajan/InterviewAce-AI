import json
import os

QUESTION_FOLDER = "dataset/questions"

OUTPUT_FILE = "dataset/questions.json"

REQUIRED_FIELDS = [
    "question_id",
    "subject",
    "topic",
    "difficulty",
    "question",
    "ideal_answer"
]


def validate_question(question):
    for field in REQUIRED_FIELDS:
        if field not in question:
            raise ValueError(
                f"Missing '{field}' in question {question.get('question_id', 'Unknown')}"
            )


def main():

    all_questions = []
    ids = set()

    for filename in os.listdir(QUESTION_FOLDER):

        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(QUESTION_FOLDER, filename)

        print(f"Reading {filename}")

        with open(filepath, "r", encoding="utf-8") as f:
            questions = json.load(f)

        for question in questions:

            validate_question(question)

            if question["question_id"] in ids:
                raise ValueError(
                    f"Duplicate Question ID : {question['question_id']}"
                )

            ids.add(question["question_id"])

            all_questions.append(question)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        json.dump(all_questions, f, indent=4, ensure_ascii=False)

    print("\nQuestion Bank Created Successfully!")

    print(f"Total Questions : {len(all_questions)}")


if __name__ == "__main__":
    main()