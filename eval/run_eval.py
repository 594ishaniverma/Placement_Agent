import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent.graph import run_workflow
from eval.ground_truth import expected_ambiguity, expected_students

POSTS = ROOT / "data" / "job_posts"


def evaluate() -> dict:
    expected_total = predicted_total = true_positives = 0
    ambiguity_correct = post_count = 0
    for path in sorted(POSTS.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        expected = set(expected_students(text))
        result = run_workflow(path.stem, text, interactive=False)
        predicted = {student["student_id"] for student in result["students"]}
        expected_total += len(expected)
        predicted_total += len(predicted)
        true_positives += len(expected & predicted)
        ambiguity_correct += expected_ambiguity(text) == result["ambiguous"]
        post_count += 1
    precision = true_positives / predicted_total if predicted_total else 1.0
    recall = true_positives / expected_total if expected_total else 1.0
    return {
        "precision": precision,
        "recall": recall,
        "ambiguity_accuracy": ambiguity_correct / post_count if post_count else 0.0,
        "posts": post_count,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
