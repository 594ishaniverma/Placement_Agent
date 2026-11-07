from pathlib import Path
import sqlite3
import re
from typing import Iterable

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "students.db"
PRIVATE_FIELDS = {"email", "phone", "address"}


def known_student_ids() -> set[str]:
    if not DB_PATH.exists():
        return set()
    with sqlite3.connect(DB_PATH) as connection:
        return {row[0] for row in connection.execute("SELECT student_id FROM students")}


def validate_student_ids(student_ids: Iterable[str]) -> list[str]:
    known = known_student_ids()
    return [student_id for student_id in student_ids if student_id in known]


def contains_private_field(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(rf"\b{field}\b", lowered) for field in PRIVATE_FIELDS)


def guard_notice(notice: str, student_ids: Iterable[str]) -> tuple[bool, list[str]]:
    errors = []
    known = known_student_ids()
    if any(student_id not in known for student_id in student_ids):
        errors.append("Notice contains an unknown student ID.")
    if contains_private_field(notice):
        errors.append("Notice contains a private field.")
    return not errors, errors
