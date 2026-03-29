import pandas as pd
import random
import uuid

# Define the question bank
QUESTIONS = [
    {
        "question_id": "math_q1",
        "concept_tag": "Decimals & Fractions",
        "question_text": "Which is larger: 0.8 or 0.355?",
        "correct_answer": "0.8"
    },
    {
        "question_id": "math_q2",
        "concept_tag": "Linear Equations",
        "question_text": "Solve for x: 2x - 5 = 11",
        "correct_answer": "x = 8"
    },
    {
        "question_id": "math_q3",
        "concept_tag": "Order of Operations",
        "question_text": "Evaluate: 4 + 3 * 2",
        "correct_answer": "10"
    },
    {
        "question_id": "math_q4",
        "concept_tag": "Negative Numbers",
        "question_text": "Calculate: -5 - (-3)",
        "correct_answer": "-2"
    },
    {
        "question_id": "math_q5",
        "concept_tag": "Exponents",
        "question_text": "Calculate: 3 squared.",
        "correct_answer": "9"
    }
]

# Define typical mistakes for the questions to generate synthetic data
MISTAKES = {
    "math_q1": [
        {"attempt": "0.355 because 355 is a bigger number than 8.", "error_type": "Conceptual", "is_correct": False},
        {"attempt": "0.8 because 8 is larger than 3.", "error_type": "None", "is_correct": True},
        {"attempt": "They are the same.", "error_type": "Factual", "is_correct": False}
    ],
    "math_q2": [
        {"attempt": "2x - 5 = 11 -> 2x = 11 - 5 = 6 -> x = 3", "error_type": "Procedural", "is_correct": False},
        {"attempt": "2x = 16 -> x = 8", "error_type": "None", "is_correct": True},
        {"attempt": "2x = 6 -> x = 3. I subtracted 5 instead of adding.", "error_type": "Procedural", "is_correct": False}
    ],
    "math_q3": [
        {"attempt": "4 + 3 = 7 -> 7 * 2 = 14", "error_type": "Conceptual", "is_correct": False},
        {"attempt": "3 * 2 = 6 -> 4 + 6 = 10", "error_type": "None", "is_correct": True},
        {"attempt": "4 + 6 = 11", "error_type": "Factual", "is_correct": False}
    ],
    "math_q4": [
        {"attempt": "-5 + 3 = -2", "error_type": "None", "is_correct": True},
        {"attempt": "-5 - 3 = -8", "error_type": "Procedural", "is_correct": False},
        {"attempt": "Minus minus makes a minus. So -5 - 3 = -8", "error_type": "Conceptual", "is_correct": False}
    ],
    "math_q5": [
        {"attempt": "3 * 2 = 6", "error_type": "Procedural", "is_correct": False},
        {"attempt": "3 * 3 = 9", "error_type": "None", "is_correct": True},
        {"attempt": "3", "error_type": "Factual", "is_correct": False}
    ]
}

def generate_data(num_records=100):
    student_ids = [f"Student_{i:03d}" for i in range(1, 21)]  # 20 students
    records = []

    for _ in range(num_records):
        student = random.choice(student_ids)
        question = random.choice(QUESTIONS)
        
        # 60% chance of making a mistake for realism
        if random.random() < 0.6:
            mistake_choices = [m for m in MISTAKES[question["question_id"]] if not m["is_correct"]]
            if not mistake_choices:
                 # fallback if no mistakes defined
                 mistake = MISTAKES[question["question_id"]][0]
            else:
                 mistake = random.choice(mistake_choices)
        else:
            correct_choices = [m for m in MISTAKES[question["question_id"]] if m["is_correct"]]
            if not correct_choices:
                 mistake = MISTAKES[question["question_id"]][0]
            else:
                 mistake = random.choice(correct_choices)

        records.append({
            "log_id": str(uuid.uuid4())[:8],
            "student_id": student,
            "question_id": question["question_id"],
            "concept_tag": question["concept_tag"],
            "question_text": question["question_text"],
            "correct_answer": question["correct_answer"],
            "student_attempt_text": mistake["attempt"],
            "error_type": mistake["error_type"],
            "is_correct": mistake["is_correct"],
            "time_to_first_response_ms": random.randint(5000, 120000), # 5s to 2min
            "hint_requests": random.randint(0, 3) if not mistake["is_correct"] else 0
        })
    df = pd.DataFrame(records)
    df.to_csv("student_logs.csv", index=False)
    print(f"✅ Successfully generated 'student_logs.csv' with {len(df)} simulated records.")

if __name__ == "__main__":
    generate_data(250)
