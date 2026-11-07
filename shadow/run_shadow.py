import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent.graph import run_workflow
POSTS_DIR = ROOT / "data" / "job_posts"
LOG_DIR = ROOT / "shadow" / "logs"


def run_shadow() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(POSTS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        result = run_workflow(path.stem, text, interactive=False)
        record = {
            "post": path.name,
            "rules": result["rules"],
            "ambiguous": result["ambiguous"],
            "ambiguity_reasons": result["ambiguity_reasons"],
            "eligible_count": len(result["students"]),
            "student_ids": [student["student_id"] for student in result["students"]],
            "draft_preview": result["draft"].splitlines()[:3],
        }
        (LOG_DIR / f"{path.stem}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"Shadow run complete: {len(list(POSTS_DIR.glob('*.txt')))} posts, no notices sent.")


if __name__ == "__main__":
    run_shadow()
