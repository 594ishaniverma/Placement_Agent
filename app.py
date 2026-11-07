from pathlib import Path
import argparse

from agent.graph import run_workflow

POSTS_DIR = Path(__file__).resolve().parent / "data" / "job_posts"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the placement notice workflow.")
    parser.add_argument("--post", required=True, help="Post number or filename stem, such as 01 or 01_clear")
    parser.add_argument("--no-interactive", action="store_true")
    args = parser.parse_args()
    matches = sorted(path for path in POSTS_DIR.glob("*.txt") if path.stem.startswith(args.post))
    if not matches:
        raise SystemExit(f"No job post matches {args.post!r}")
    path = matches[0]
    result = run_workflow(path.stem, path.read_text(encoding="utf-8"), not args.no_interactive)
    print(f"\nAmbiguous: {result['ambiguous']}")
    print(f"Eligible students: {len(result['students'])}")
    print(f"Approved: {result['approved']}")


if __name__ == "__main__":
    main()
