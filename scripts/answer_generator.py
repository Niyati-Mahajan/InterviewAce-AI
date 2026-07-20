import random

LABELS = [
    ("Excellent", (9, 10)),
    ("Good", (7, 8)),
    ("Average", (5, 6)),
    ("Poor", (3, 4)),
    ("Very Poor", (1, 2))
]

VERY_POOR = [
    "I don't know.",
    "No idea.",
    "Not sure.",
    "I haven't learned this.",
    "Can't answer this question."
]

POOR = [
    "I think it is related to programming.",
    "It is something used in computers.",
    "It is used for coding.",
    "I have heard about it but don't remember.",
    "It is a software."
]

AVERAGE_PREFIX = [
    "It is",
    "It can be defined as",
    "Basically",
    "In simple words",
    "It refers to"
]

GOOD_PREFIX = [
    "Python interview answer:",
    "The concept refers to",
    "This can be explained as",
    "Technically,"
]
def shorten_answer(ideal_answer, percent):
    words = ideal_answer.split()

    keep = max(5, int(len(words) * percent))

    return " ".join(words[:keep])


def generate_answer(ideal_answer, label):

    if label == "Excellent":
        return ideal_answer

    elif label == "Good":
        return random.choice(GOOD_PREFIX) + " " + shorten_answer(ideal_answer, 0.75)

    elif label == "Average":
        return random.choice(AVERAGE_PREFIX) + " " + shorten_answer(ideal_answer, 0.45)

    elif label == "Poor":
        return random.choice(POOR)

    else:
        return random.choice(VERY_POOR)