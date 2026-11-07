from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def load_skill(name: str) -> str:
    path = SKILLS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Unknown skill: {name}")
    return path.read_text(encoding="utf-8")
