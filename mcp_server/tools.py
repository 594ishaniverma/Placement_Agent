from pathlib import Path
import sqlite3
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "students.db"
ALLOWED_TABLES = {"students"}
MAX_ROWS = 500
ALLOWED_COLUMNS = {
    "students": {
        "student_id", "name", "email", "branch", "cgpa", "tenth_percent",
        "twelfth_percent", "graduation_year", "backlogs", "placed", "phone",
    }
}


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def list_schema() -> list[dict[str, Any]]:
    with connect() as connection:
        return [
            {"name": row["name"], "type": row["type"]}
            for row in connection.execute("PRAGMA table_info(students)")
        ]


def query_eligible_students(filters: dict[str, Any], limit: int = 100) -> list[dict[str, Any]]:
    safe_limit = max(1, min(limit, MAX_ROWS))
    clauses = []
    parameters: list[Any] = []
    for column, value in filters.items():
        if column not in ALLOWED_COLUMNS["students"]:
            raise ValueError(f"Column {column!r} is not public.")
        if isinstance(value, dict):
            operator = value.get("operator")
            operand = value.get("value")
            operators = {"gte": ">=", "lte": "<=", "gt": ">", "lt": "<", "eq": "="}
            if operator not in operators:
                raise ValueError("Unsupported filter operator.")
            clauses.append(f"{column} {operators[operator]} ?")
            parameters.append(operand)
        else:
            clauses.append(f"{column} = ?")
            parameters.append(value)
    sql = "SELECT student_id, name, branch, cgpa, tenth_percent, twelfth_percent, graduation_year, backlogs, placed FROM students"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += f" LIMIT {safe_limit}"
    with connect() as connection:
        return [dict(row) for row in connection.execute(sql, parameters)]


def get_student_count() -> int:
    with connect() as connection:
        return connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]


def validate_table(table: str) -> None:
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Table {table!r} is not allowlisted.")
