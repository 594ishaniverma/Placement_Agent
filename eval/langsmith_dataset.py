import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from eval.ground_truth import expected_ambiguity, expected_students


def build_examples() -> list[dict]:
    posts_dir = ROOT / "data" / "job_posts"
    examples = []
    for path in sorted(posts_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        examples.append({
            "id": path.stem,
            "inputs": {"post": text},
            "outputs": {
                "eligible_student_ids": expected_students(text),
                "ambiguous": expected_ambiguity(text),
            },
        })
    return examples


if __name__ == "__main__":
    print(json.dumps(build_examples(), indent=2))
    if os.getenv("LANGSMITH_API_KEY"):
        try:
            from langsmith import Client
            client = Client()
            dataset_name = os.getenv("LANGSMITH_PROJECT", "placement-agent")
            dataset = client.create_dataset(dataset_name=dataset_name)
            for example in build_examples():
                client.create_example(
                    inputs=example["inputs"],
                    outputs=example["outputs"],
                    dataset_id=dataset.id,
                )
            print(f"Uploaded {len(build_examples())} examples to LangSmith.")
        except ImportError as error:
            print(f"LangSmith upload skipped: {error}")
