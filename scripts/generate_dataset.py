# Step 1
import json
import csv
import random

from answer_generator import generate_answer, LABELS

INPUT_FILE = "dataset/questions.json"
OUTPUT_FILE = "dataset/dataset.csv"

# Step 4
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

# Step 5  👇👇👇
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "question_id",
        "subject",
        "topic",
        "difficulty",
        "question",
        "ideal_answer",
        "student_answer",
        "score",
        "label"
    ])

    for q in questions:

        for label, score_range in LABELS:

            score = random.randint(score_range[0], score_range[1])

            student = generate_answer(
                q["ideal_answer"],
                label
            )

            writer.writerow([
                q["question_id"],
                q["subject"],
                q["topic"],
                q["difficulty"],
                q["question"],
                q["ideal_answer"],
                student,
                score,
                label
            ])

print("Dataset Generated Successfully!")